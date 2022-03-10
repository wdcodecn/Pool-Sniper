
from core.common import get_logger
from contracts.sniperV3 import SniperContract
from core.chain_network import ChainNetwork
from core.eoa_account import EoaAccount
from core.chain_account import ChainAccount
from wconfig import SNIPER, HDWallet_01
import time
logger = get_logger('sniperswap.log')

chain_name = 'bsc'
gas_price = 20

chain = ChainNetwork(chain_name=chain_name)
for i in range(1, 100):
    i = 400 - i
    eoa = EoaAccount(address=HDWallet_01.get_hd_address(i), prikey=HDWallet_01.get_hd_privatekey(i))

    chain_account = ChainAccount(account=eoa, chain=chain)
    sniper_addr = SNIPER[chain_name]
    sniper = SniperContract(chain=chain, address=sniper_addr)

    tx_params = sniper.swap()
    [tx_signed, current_nonce] = chain_account.sign(txn=tx_params, gas_price=gas_price)
    chain_account.push(tx_signed=tx_signed)
    time.sleep(1)