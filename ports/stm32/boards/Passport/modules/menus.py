# SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# menus.py - Menu configuration

import lvgl as lv
from utils import has_seed
from pages import ColorPickerPage


def manage_account_menu():
    from flows import RenameAccountFlow, DeleteAccountFlow, ConnectWalletFlow
    from pages import AccountDetailsPage

    return [
        {'icon': lv.ICON_FOLDER, 'label': 'Account Details', 'page': AccountDetailsPage},
        {'icon': lv.ICON_INFO, 'label': 'Rename Account', 'flow': RenameAccountFlow},
        {'icon': lv.ICON_CONNECT, 'label': 'Connect Wallet', 'flow': ConnectWalletFlow,
         'statusbar': {'title': 'CONNECT'}},
        {'icon': lv.ICON_CANCEL, 'label': 'Delete Account', 'flow': DeleteAccountFlow},
    ]


def account_menu():
    from flows import VerifyAddressFlow, SignPsbtQRFlow, SignPsbtMicroSDFlow

    return [
        {'icon': lv.ICON_SCAN_QR, 'label': 'Sign with QR Code', 'flow': SignPsbtQRFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_MICROSD, 'label': 'Sign with microSD', 'flow': SignPsbtMicroSDFlow,
         'statusbar': {'title': 'SIGN'}},
        {'icon': lv.ICON_VERIFY_ADDRESS, 'label': 'Verify Address', 'flow': VerifyAddressFlow},
        {'icon': lv.ICON_FOLDER, 'label': 'Manage Account', 'submenu': manage_account_menu},
    ]


def plus_menu():
    from flows import NewAccountFlow, ApplyPassphraseFlow
    return [
        {'icon': lv.ICON_ADD_ACCOUNT, 'label': 'New Account', 'flow': NewAccountFlow},
        {'icon': lv.ICON_PASSPHRASE, 'label': 'Enter Passphrase', 'flow': ApplyPassphraseFlow,
         'statusbar': {'title': 'PASSPHRASE'}},
    ]


def device_menu():
    from flows import AboutFlow, ChangePINFlow
    from pages import AutoShutdownSettingPage, BrightnessSettingPage
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_BRIGHTNESS, 'label': 'Screen Brightness', 'page': BrightnessSettingPage},
        {'icon': lv.ICON_COUNTDOWN, 'label': 'Auto-Shutdown', 'page': AutoShutdownSettingPage},
        {'icon': lv.ICON_PIN, 'label': 'Change PIN', 'flow': ChangePINFlow, 'is_visible': is_logged_in},
        {'icon': lv.ICON_INFO, 'label': 'About', 'flow': AboutFlow},
    ]


def backup_menu():
    from flows import BackupFlow, RestoreBackupFlow, VerifyBackupFlow, ViewBackupCodeFlow

    return [
        {'icon': lv.ICON_BACKUP, 'label': 'Backup Now', 'flow': BackupFlow, 'is_visible': has_seed},
        {'icon': lv.ICON_RETRY, 'label': 'Restore', 'flow': RestoreBackupFlow,
         'args': {'refresh_cards_when_done': True}},
        {'icon': lv.ICON_CIRCLE_CHECK, 'label': 'Verify Backup', 'flow': VerifyBackupFlow},
        {'icon': lv.ICON_PIN, 'label': 'View Backup Code', 'flow': ViewBackupCodeFlow,
            'statusbar': {'title': 'BACKUP', 'icon': lv.ICON_PIN}, 'is_visible': has_seed}
    ]


def bitcoin_menu():
    from flows import SetChainFlow
    from pages import UnitsSettingPage
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_BITCOIN, 'label': 'Units', 'page': UnitsSettingPage, 'is_visible': is_logged_in},
        {'icon': lv.ICON_TWO_KEYS, 'label': 'Multisig', 'submenu': multisig_menu, 'is_visible': has_seed},
        {'icon': lv.ICON_NETWORK, 'label': 'Testnet', 'flow': SetChainFlow, 'statusbar': {},
         'is_visible': is_logged_in},
    ]


def security_menu():
    from flows import ChangePINFlow, SignTextFileFlow, ViewSeedWordsFlow, NewSeedFlow, RestoreSeedFlow

    return [
        {'icon': lv.ICON_SEED, 'label': 'Restore Seed', 'flow': RestoreSeedFlow, 'is_visible': lambda: not has_seed(),
         'args': {'refresh_cards_when_done': True}},
        {'icon': lv.ICON_SEED, 'label': 'New Seed', 'flow': NewSeedFlow, 'is_visible': lambda: not has_seed(),
         'args': {'refresh_cards_when_done': True}},
        {'icon': lv.ICON_SIGN, 'label': 'Sign Text File', 'flow': SignTextFileFlow, 'is_visible': has_seed},
    ]


def update_menu():
    from flows import UpdateFirmwareFlow, ViewCurrentFirmwareFlow
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_FIRMWARE, 'label': 'Update Firmware', 'flow': UpdateFirmwareFlow, 'is_visible': is_logged_in},
        {'icon': lv.ICON_INFO, 'label': 'Current Version', 'flow': ViewCurrentFirmwareFlow, 'statusbar': {}},
    ]


def microsd_menu():
    from flows import FormatMicroSDFlow, ListFilesFlow, ExportSummaryFlow

    return [
        {'icon': lv.ICON_MICROSD, 'label': 'Format Card', 'flow': FormatMicroSDFlow},
        {'icon': lv.ICON_FILE, 'label': 'List Files', 'flow': ListFilesFlow},
        {'icon': lv.ICON_INFO, 'label': 'Export Summary', 'flow': ExportSummaryFlow, 'is_visible': has_seed},
    ]


def multisig_item_menu():
    from flows import RenameMultisigFlow, DeleteMultisigFlow, ViewMultisigDetailsFlow

    return [
        {'icon': lv.ICON_TWO_KEYS, 'label': 'View Details', 'flow': ViewMultisigDetailsFlow},
        {'icon': lv.ICON_TWO_KEYS, 'label': 'Rename', 'flow': RenameMultisigFlow},
        {'icon': lv.ICON_TWO_KEYS, 'label': 'Delete', 'flow': DeleteMultisigFlow},
    ]


def multisig_menu():
    from multisig_wallet import MultisigWallet
    from pages import MultisigPolicySettingPage, ErrorPage
    from flows import ImportMultisigWalletFromMicroSDFlow, ImportMultisigWalletFromQRFlow

    if not MultisigWallet.exists():
        items = [{'icon': lv.ICON_TWO_KEYS, 'label': '(None setup yet)', 'page': ErrorPage,
                  'args': {'text': "You haven't imported any multisig wallets yet."}}]
    else:
        items = []
        for ms in MultisigWallet.get_all():
            nice_name = '%d/%d: %s' % (ms.M, ms.N, ms.name)
            items.append({
                'icon': lv.ICON_TWO_KEYS,
                'label': nice_name,
                'submenu': multisig_item_menu,
                # Adding this below causes the header to stick around after it shoudl be gone
                # Probably need MenuFlow() to pop it off after
                # 'args': {'card_header': {'title': nice_name}, 'context': ms.storage_idx}
                'args': {'context': ms.storage_idx}
            })

    items.append({'icon': lv.ICON_SCAN_QR, 'label': 'Import from QR', 'flow': ImportMultisigWalletFromQRFlow})
    items.append({'icon': lv.ICON_MICROSD, 'label': 'Import from microSD',
                  'flow': ImportMultisigWalletFromMicroSDFlow})
    items.append({'icon': lv.ICON_SETTINGS, 'label': 'Multisig Policy', 'page': MultisigPolicySettingPage})

    return items


def developer_pubkey_menu():
    from utils import has_dev_pubkey
    from flows import InstallDevPubkeyFlow, ViewDevPubkeyFlow, RemoveDevPubkeyFlow

    return [
        {'icon': lv.ICON_ONE_KEY, 'label': 'Install PubKey', 'flow': InstallDevPubkeyFlow,
         'is_visible': lambda: not has_dev_pubkey()},
        {'icon': lv.ICON_ONE_KEY, 'label': 'View PubKey', 'flow': ViewDevPubkeyFlow,
         'is_visible': has_dev_pubkey},
        {'icon': lv.ICON_CANCEL, 'label': 'Remove Pubkey', 'flow': RemoveDevPubkeyFlow,
         'is_visible': has_dev_pubkey}
    ]


def advanced_menu():
    from flows import ViewSeedWordsFlow, ErasePassportFlow
    from pages import ShowSecurityWordsSettingPage

    return [
        {'icon': lv.ICON_SETTINGS, 'label': 'Security Words', 'page': ShowSecurityWordsSettingPage},
        {'icon': lv.ICON_SEED, 'label': 'View Seed Words', 'flow': ViewSeedWordsFlow, 'is_visible': has_seed},
        {'icon': lv.ICON_ONE_KEY, 'label': 'Developer Pubkey', 'submenu': developer_pubkey_menu,
         'statusbar': {'title': 'DEV. PUBKEY'}},
        {'icon': lv.ICON_MICROSD, 'label': 'microSD', 'submenu': microsd_menu},
        {'icon': lv.ICON_ERASE, 'label': 'Erase Passport', 'flow': ErasePassportFlow},
    ]


# def developer_menu():
#     from flows import (
#         ScvFlow,
#         LoginFlow,
#         NewSeedFlow,
#         SetInitialPINFlow,
#         DeveloperFunctionsFlow,
#         ResetPINFlow,
#         SpinDelayFlow
#     )
#     from pages import BatteryPage, StatusPage, ShowQRPage
#     from data_codecs.qr_type import QRType

#     return [
#         {'icon': lv.ICON_BATTERY, 'label': 'Battery', 'page': BatteryPage},
#         {'icon': lv.ICON_ERASE, 'label': 'Factory Reset',
#             'flow': DeveloperFunctionsFlow, 'args': {'fn_name': 'factory_reset'}},
#         {'icon': lv.ICON_RETRY, 'label': 'Spin!!!', 'flow': SpinDelayFlow, 'args': {'delay_ms': 10000}},
#         {'icon': lv.ICON_SETTINGS, 'label': 'Dump Settings',
#             'flow': DeveloperFunctionsFlow, 'args': {'fn_name': 'dump_settings'}},
#         {'icon': lv.ICON_SCAN_QR, 'label': 'Show Setup QR', 'page': StatusPage, 'args': {
#             'text': 'Scan the QR code above with Envoy.', 'icon': lv.LARGE_ICON_SETUP_QR}, 'card_header': {}},
#         {'icon': lv.ICON_SCAN_QR, 'label': 'Show Test UR', 'page': ShowQRPage, 'args': {
#             'qr_type': QRType.UR2, 'qr_data': 'sdflkajd lkajdslkajdslkajsdkajdlkajsdflkajdslkjasdlkjadsflkajsdsdfl' +
#             'lkajdslkajdslkajsdkajdlkajsdflkajdslkjasdlkjadsflkajsdflksdflkajd lkajdslkajdslkajsdkajdlkajsdajdslkj' +
#             'asdlkjadsflkajsdflksdflkajd lkajdslkajdslkajsdkajdlkajsdflkajdslkjasdlkjadsflkajsdflksdflkajd lkajds' +
#             'lkajdslkajsdkajdlkajsdflkajdslkjasdlkja'}},
#         {'icon': lv.ICON_SHIELD, 'label': 'Supply Chain', 'flow': ScvFlow},
#         {'icon': lv.ICON_ONE_KEY, 'label': 'Login', 'flow': LoginFlow},
#         {'icon': lv.ICON_SEED, 'label': 'New Seed', 'flow': NewSeedFlow, 'args': {'refresh_cards_when_done': True}},
#         {'icon': lv.ICON_CHANGE_PIN, 'label': 'Set PIN', 'flow': SetInitialPINFlow},
#         {'icon': lv.ICON_CHANGE_PIN, 'label': 'Reset PIN', 'flow': ResetPINFlow},
#         # {'icon': lv.ICON_SETTINGS, 'label': 'I\'m Busy!', 'page': LongTextPage,
#         #     'args': {'show_busy': True, 'message': 'Signing Transaction...'}},
#         # {'icon': lv.ICON_SETTINGS, 'label': 'FCC Test', 'flow': FCCTestFlow},
#         # {'icon': lv.ICON_ABOUT, 'label': 'Color Picker', 'page': ColorPickerPage},
#         # {'icon': lv.ICON_CHANGE_PIN, 'label': 'Enter PIN', 'page': PINEntryPage,
#         #  'args': {'title': 'Enter Initial PIN'}},
#         # {'icon': lv.ICON_FOLDER, 'label': 'Rename Account', 'page': TextInputPage,
#         #     'args': {'card_header': {'title': 'Rename Account', 'icon': lv.ICON_ABOUT, 'right_text': '!!',
#         #              'bg_color': RED, 'fg_color': FD_BLUE}}},
#         # {'icon': lv.ICON_SEED, 'label': 'Enter Seed', 'page': PredictiveTextInputPage},
#         # {'icon': lv.ICON_CHANGE_PIN, 'label': 'Enter Backup Code', 'page': BackupCodePage},
#     ]


def settings_menu():
    from utils import is_logged_in

    return [
        {'icon': lv.ICON_DEVICE, 'label': 'Device', 'submenu': device_menu},
        {'icon': lv.ICON_BACKUP, 'label': 'Backup', 'submenu': backup_menu, 'is_visible': is_logged_in},
        {'icon': lv.ICON_FIRMWARE, 'label': 'Firmware', 'submenu': update_menu},
        {'icon': lv.ICON_BITCOIN, 'label': 'Bitcoin', 'submenu': bitcoin_menu, 'is_visible': is_logged_in},
        {'icon': lv.ICON_ADVANCED, 'label': 'Advanced', 'submenu': advanced_menu, 'is_visible': is_logged_in},
        # {'icon': lv.ICON_ADVANCED, 'label': 'Developer', 'submenu': developer_menu, 'is_visible': is_logged_in},
    ]
