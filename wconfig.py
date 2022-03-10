import os
import logging
from core.chain_account import EoaAccount

from core.wallets.ETHAddressDB import EthAddressDB

env_dist = os.environ

DATA_PATH = env_dist.get('DATA_PATH') if env_dist.get('DATA_PATH') else "data"
LOG_PATH = env_dist.get('LOG_PATH') if env_dist.get('LOG_PATH') else f"/tmp/"


LOG_LEVEL = logging.DEBUG



CHAIN_PROVIDER = {
    "eth":'https://api.mycryptoapi.com/eth', }

ACCOUNT1   = EoaAccount('address', 'privatekey')


HTTP_PROXY_URL = ''

# sniper contract address
SNIPER = {
    'bsc': '',
    'bsctest': '',
    'matic': ' ',
    'kovan': '0x29f570452531688590eC4e4F80fB27Bbb52e2131',
    'avax': ' '
}


#
mnemonic = ''
HDWallet_01 = EthAddressDB(mnemonic)