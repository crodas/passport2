# SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2018 Coinkite, Inc. <coldcardwallet.com>
# SPDX-License-Identifier: GPL-3.0-only
#
# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#
# verify_address_flow.py - Scan an address QR code and verify that it belongs to this Passport.


from flows import Flow
from common import ui
import microns


RECEIVE_ADDR = 0
CHANGE_ADDR = 1
NUM_TO_CHECK = 10


class VerifyAddressFlow(Flow):
    def __init__(self, sig_type=None, multisig_wallet=None):
        if sig_type is not None:
            initial_state = self.scan_address
        else:
            initial_state = self.choose_sig_type

        super().__init__(initial_state=initial_state, name='VerifyAddressFlow')
        self.account = ui.get_active_account()
        self.acct_num = self.account.get('acct_num')
        self.sig_type = sig_type
        self.multisig_wallet = multisig_wallet
        self.is_multisig = False
        self.found_addr_idx = None
        self.found_is_change = False
        self.addr_type = None
        self.deriv_path = None
        self.address = None

        # These can't be properly initialized until we know more about the address
        self.low_range = None
        self.high_range = None
        self.low_size = [0, 0]
        self.high_size = [0, 0]

    async def choose_sig_type(self):
        from pages import SinglesigMultisigChooserPage
        from multisig_wallet import MultisigWallet

        if MultisigWallet.get_count() == 0:
            self.sig_type = 'single-sig'
            self.goto(self.scan_address, save_curr=False)  # Don't save this since we're skipping this state
        else:
            result = await SinglesigMultisigChooserPage(
                initial_value=self.sig_type).show()
            if result is None:
                if not self.back():
                    self.set_result(False)
                return

            (self.sig_type, self.multisig_wallet) = result
            # print('sig_type={}'.format(self.sig_type))
            # print('multisig_wallet={}'.format(self.multisig_wallet))
            self.goto(self.scan_address)

    async def scan_address(self):
        import chains
        from pages import ErrorPage, ScanQRPage
        from wallets.utils import get_addr_type_from_address, get_deriv_path_from_addr_type_and_acct
        from utils import is_valid_btc_address, get_next_addr

        result = await ScanQRPage(
            left_micron=microns.Back,
            right_micron=None).show()
        if result is None or result.error is not None:
            # User canceled the scan or bad QR code
            if not self.back():
                self.set_result(False)
            return

        # print('result={}'.format(result))
        self.address = result.data

        # Simple check on the data type first
        chain_name = chains.current_chain().name
        self.address, is_valid_btc = is_valid_btc_address(self.address)
        if not is_valid_btc:
            await ErrorPage("Not a valid {} address.".format(chain_name)).show()
            return

        # Get the address type from the address
        self.is_multisig = self.sig_type == 'multisig'

        # print('address={} acct_num={} is_multisig={}'.format(address, self.acct_num, is_multisig))
        self.addr_type = get_addr_type_from_address(self.address, self.is_multisig)
        self.deriv_path = get_deriv_path_from_addr_type_and_acct(self.addr_type, self.acct_num, self.is_multisig)

        # Setup initial ranges
        a = [get_next_addr(self.acct_num, self.addr_type, False), get_next_addr(self.acct_num, self.addr_type, True)]
        self.low_range = [(a[RECEIVE_ADDR], a[RECEIVE_ADDR]), (a[CHANGE_ADDR], a[CHANGE_ADDR])]
        self.high_range = [(a[RECEIVE_ADDR], a[RECEIVE_ADDR]), (a[CHANGE_ADDR], a[CHANGE_ADDR])]

        self.goto(self.search_for_address)

    async def search_for_address(self):
        from tasks import search_for_address_task
        from utils import get_prev_address_range, get_next_address_range, spinner_task

        # Try next batch of addresses
        for is_change in range(0, 2):
            self.low_range[is_change], self.low_size[is_change] = get_prev_address_range(self.low_range[is_change],
                                                                                         NUM_TO_CHECK // 2)
            self.high_range[is_change], self.high_size[is_change] = get_next_address_range(
                self.high_range[is_change], NUM_TO_CHECK - self.low_size[is_change])

        addr_idx = -1
        is_change = 0

        for is_change in range(0, 2):
            # print('CHECKING: low_range={}  low_size={}'.format(self.low_range, self.low_size))
            # Check downwards
            if self.low_size[is_change] > 0:
                (addr_idx, path_info, error) = await spinner_task(
                    'Searching Addresses',
                    search_for_address_task,
                    args=[self.deriv_path,
                          self.low_range[is_change][0],
                          self.address,
                          self.addr_type,
                          self.multisig_wallet,
                          is_change,
                          self.low_size[is_change],
                          True])

            # Exit if already found
            if addr_idx >= 0:
                break

            # print('CHECKING: high_range={}  high_size={}'.format(self.high_range, self.high_size))
            # Check upwards
            (addr_idx, path_info, error) = await spinner_task(
                'Searching Addresses',
                search_for_address_task,
                args=[self.deriv_path,
                      self.high_range[is_change][0],
                      self.address,
                      self.addr_type,
                      self.multisig_wallet,
                      is_change,
                      self.high_size[is_change],
                      True])

            if addr_idx >= 0:
                break

        if addr_idx >= 0:
            self.found_addr_idx = addr_idx
            self.found_is_change = is_change == 1
            self.goto(self.found)
        else:
            self.goto(self.not_found)

    async def not_found(self):
        from pages import ErrorPage

        # Address was not found in that batch of 100, so offer to keep searching
        msg = 'Address Not Found\nRanges Checked:\n'

        # Build a merged range for receive and one for change addresses
        merged_range = []
        for is_change in range(0, 2):
            msg += '{} addrs: {}-{}{}'.format(
                'Change' if is_change == 1 else 'Receive', self.low_range[is_change][0],
                self.high_range[is_change][1] - 1, '' if is_change == 1 else '\n')

        msg += '\n\nContinue searching?'

        result = await ErrorPage(msg, left_micron=microns.Cancel, right_micron=microns.Checkmark).show()
        if result:
            self.goto(self.search_for_address)
        else:
            self.set_result(False)

    async def found(self):
        from pages import SuccessPage
        from utils import save_next_addr, format_btc_address

        # Remember where to start from next time
        save_next_addr(self.acct_num, self.addr_type, self.found_addr_idx, self.found_is_change)
        address = format_btc_address(self.address, self.addr_type)

        msg = '''{}

{} Address {}'''.format(
            self.address,
            'Change' if self.found_is_change == 1 else 'Receive',
            self.found_addr_idx)

        await SuccessPage(msg).show()
        self.set_result(True)
