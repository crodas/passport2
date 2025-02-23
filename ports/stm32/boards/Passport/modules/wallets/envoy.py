# SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# envoy.py - Envoy support
#

import stash
import ujson
import chains
from utils import to_str, get_accounts
from data_codecs.qr_type import QRType
from public_constants import AF_CLASSIC, AF_P2WPKH

# from .multisig_json import create_multisig_json_wallet
# from .multisig_import import read_multisig_config_from_qr, read_multisig_config_from_microsd
from .utils import get_bip_num_from_addr_type


def create_envoy_export(sw_wallet=None, addr_type=None, acct_num=0, multisig=False, legacy=False, export_mode='qr'):
    # Generate line-by-line JSON details about wallet.
    #
    # Adapted from Electrum format, but simplified for Envoy use
    from common import settings, system

    serial_num = system.get_serial_number()
    fw_version = 'v{}'.format(system.get_software_info()[0])

    mode = get_bip_num_from_addr_type(addr_type, multisig)

    chain = chains.current_chain()

    with stash.SensitiveValues() as sv:
        acct_path = "m/{mode}'/{coin}'/{acct}'".format(
            mode=mode,
            coin=chain.b44_cointype,
            acct=acct_num)

        child_node = sv.derive_path(acct_path)
        xfp = settings.get('xfp')
        xpub = sv.chain.serialize_public(child_node, AF_CLASSIC)
        # print('xfp to export: {}'.format(xfp))
        # print('xpub to export: {}'.format(xpub))

    accounts = get_accounts()
    act_name = None
    if accounts is not None and len(accounts) > 0:
        for acct in accounts:
            if acct.get('acct_num') == acct_num:
                acct_name = acct.get('name', None)
                break

    rv = dict(derivation=acct_path,
              xfp=xfp,
              xpub=xpub,
              acct_name=acct_name,
              acct_num=acct_num,
              hw_version=1.2,
              fw_version=fw_version,
              serial=serial_num)

    # Return the possible account mappings that the exported wallet can choose from
    # When we get the address back, we can determine the 'fmt' from the address and then look it up to
    # find the derivation path and account number.
    accts = [{'fmt': addr_type, 'deriv': acct_path, 'acct': acct_num}]

    msg = ujson.dumps(rv)
    # print('msg={}'.format(to_str(msg)))
    return (msg, accts)


EnvoyWallet = {
    'label': 'Envoy',
    'sig_types': [
        {'id': 'single-sig', 'label': 'Single-sig', 'addr_type': AF_P2WPKH, 'create_wallet': create_envoy_export},
    ],
    'export_modes': [
        {'id': 'qr', 'label': 'QR Code', 'qr_type': QRType.UR2}
    ],
    'skip_address_validation': False,
    'skip_multisig_import': True,
}
