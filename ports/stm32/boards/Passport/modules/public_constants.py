# SPDX-FileCopyrightText: 2020 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2018 Coinkite, Inc. <coldcardwallet.com>
# SPDX-License-Identifier: GPL-3.0-only
#
# Constants and various "limits" shared between embedded and desktop USB protocol
#
try:
    from micropython import const
except ImportError:
    const = int

from constants import PSBT_MAX_SIZE

# Max PSBT txn we support (896k as PSBT)
# - the max on the wire for mainnet is 100k
# - but a PSBT might contain a full txn for each input
MAX_TXN_LEN = PSBT_MAX_SIZE // 2
TXN_INPUT_OFFSET = 0
TXN_OUTPUT_OFFSET = MAX_TXN_LEN

# Max length of text messages for signing
MSG_SIGNING_MAX_LENGTH = const(240)

# Types of user auth we support
USER_AUTH_TOTP = const(1)       # RFC6238
USER_AUTH_HOTP = const(2)       # RFC4226
USER_AUTH_HMAC = const(3)       # PBKDF2('hmac-sha256', secret, sha256(psbt), PBKDF2_ITER_COUNT)
USER_AUTH_SHOW_QR = const(0x80)  # show secret on Passport screen (best for TOTP enroll)

MAX_USERNAME_LEN = 16
PBKDF2_ITER_COUNT = 2500

# Max depth for derived keys, in PSBT files, and USB commands
MAX_PATH_DEPTH = const(12)

# Bitmask used in sign_transaction (stxn) command
STXN_FINALIZE = const(0x01)
STXN_VISUALIZE = const(0x02)
STXN_SIGNED = const(0x04)
STXN_FLAGS_MASK = const(0x07)

# Bit values for address types
AFC_PUBKEY = const(0x01)       # pay to hash of pubkey
AFC_SEGWIT = const(0x02)       # requires a witness to spend
AFC_BECH32 = const(0x04)       # just how we're encoding it?
AFC_SCRIPT = const(0x08)       # paying into a script
AFC_WRAPPED = const(0x10)       # for transition/compat types for segwit vs. old

# Numeric codes for specific address types
AF_CLASSIC = AFC_PUBKEY          # 1addr
AF_P2SH = AFC_SCRIPT          # classic multisig / simple P2SH / 3hash
AF_P2WPKH = AFC_PUBKEY | AFC_SEGWIT | AFC_BECH32     # bc1qsdklfj
AF_P2WSH = AFC_SCRIPT | AFC_SEGWIT | AFC_BECH32     # segwit multisig
AF_P2WPKH_P2SH = AFC_WRAPPED | AFC_PUBKEY | AFC_SEGWIT     # looks classic P2SH, but p2wpkh inside
AF_P2WSH_P2SH = AFC_WRAPPED | AFC_SCRIPT | AFC_SEGWIT     # looks classic P2SH, segwit multisig

SUPPORTED_ADDR_FORMATS = frozenset([
    AF_CLASSIC,
    AF_P2SH,
    AF_P2WPKH,
    AF_P2WSH,
    AF_P2WPKH_P2SH,
    AF_P2WSH_P2SH,
])

# BIP-174 aka PSBT defined values
#
PSBT_GLOBAL_UNSIGNED_TX = const(0)
PSBT_GLOBAL_XPUB = const(1)

PSBT_IN_NON_WITNESS_UTXO = const(0)
PSBT_IN_WITNESS_UTXO = const(1)
PSBT_IN_PARTIAL_SIG = const(2)
PSBT_IN_SIGHASH_TYPE = const(3)
PSBT_IN_REDEEM_SCRIPT = const(4)
PSBT_IN_WITNESS_SCRIPT = const(5)
PSBT_IN_BIP32_DERIVATION = const(6)
PSBT_IN_FINAL_SCRIPTSIG = const(7)
PSBT_IN_FINAL_SCRIPTWITNESS = const(8)

PSBT_OUT_REDEEM_SCRIPT = const(0)
PSBT_OUT_WITNESS_SCRIPT = const(1)
PSBT_OUT_BIP32_DERIVATION = const(2)

# Bitcoin limitation: max number of signatures in CHECK_MULTISIG
# - 520 byte redeem script limit <= 15*34 bytes per pubkey == 510 bytes
# - serializations of M/N in redeem scripts assume this range
MAX_SIGNERS = const(15)

# PSBT Xpub trust policies
TRUST_VERIFY = const(0)
TRUST_OFFER = const(1)
TRUST_PSBT = const(2)


# EOF
