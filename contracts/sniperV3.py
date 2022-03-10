
from core.chain_network import ChainNetwork
from core.contract import Contract
from contracts.erc20 import ERC20Contract
from core.libs import TokenWei, AddressType
from core.libs import load_abi
import datetime
from datetime import timezone


class SniperContract(Contract):
    def __init__(self,
                 chain: ChainNetwork,
                 address: AddressType
                 ) -> None:
        self.app_name = 'sushi miso'
        self.address = chain.w3.toChecksumAddress(address)
        self.chain = chain
        self.abi = load_abi('sniperv3.json')
        self.contract = chain.w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def showparams(self, ) -> list:
        router = self.contract.functions.get23router().call()
        toaddr = self.contract.functions.get23toaddr().call()
        pair = self.contract.functions.getpairaddr().call()
        tokenin = self.contract.functions.gettokenin().call()
        tokenout = self.contract.functions.gettokenout().call()
        minReserveIn = self.contract.functions.getminReserveIn().call()
        amountIn = self.contract.functions.getamountIn().call()
        amountOutMin = self.contract.functions.getamountOutMin().call()
        self.logger.info(f"sniper address {self.address }")
        self.logger.info(f"sniper router: {router}  ")
        self.logger.info(f"sniper to: {toaddr} ")
        self.logger.info(f"sniper pair: {pair}")
        self.logger.info(f"sniper tokenin: {tokenin}  ")
        self.logger.info(f"sniper tokenout: {tokenout}   ")
        self.logger.info(f"sniper amountIn: {amountIn} Wei  ")
        self.logger.info(f"sniper minReserveIn: {minReserveIn} Wei  ")
        self.logger.info(f"sniper amountOutMin: {amountOutMin} Wei  ")
        return [router,toaddr ,pair,tokenin,tokenout,minReserveIn,amountIn ,amountOutMin]

    def showparams_more(self, tokenin_dec, tokenout_dec) -> list:
        amountIn = self.contract.functions.getamountIn().call()/10**tokenin_dec
        minReserveIn = self.contract.functions.getminReserveIn().call()/10**tokenin_dec
        amountOutMin = self.contract.functions.getamountOutMin().call()/10**tokenout_dec
        self.logger.info(f"sniper amountIn {amountIn}Token amountOutMin: {amountOutMin}Token | minReserveIn: {minReserveIn}Token ")


    def getamountOutMin(self, decimal):
        amountOutMin = self.contract.functions.getamountOutMin().call()
        amountOutMin = amountOutMin / 10**decimal
        self.logger.info(f"sniper amountOutMin: {amountOutMin}   ")
        return amountOutMin


    def swap(self ):
        gas = 500000
        func = self.contract.functions.swap()
        tx_param = self._build_tx(func, gas=gas)
        return tx_param


    def swapfee(self):
        gas = 500000
        func = self.contract.functions.swapfee()
        tx_param = self._build_tx(func, gas=gas)
        return tx_param


    def setparams(self, minReserveIn, amountIn,  amountOutMin,  tokenIn,  tokenOut,  pairaddr, uniRouter,  toaddr):
        gas = 200000
        minReserveIn=int(minReserveIn)
        amountIn=int(amountIn)
        amountOutMin=int(amountOutMin)
        tokenIn = self.chain.w3.toChecksumAddress(tokenIn)
        tokenOut = self.chain.w3.toChecksumAddress(tokenOut)
        pairaddr = self.chain.w3.toChecksumAddress(pairaddr)
        uniRouter = self.chain.w3.toChecksumAddress(uniRouter)
        toaddr = self.chain.w3.toChecksumAddress(toaddr)

        if [uniRouter,toaddr ,pairaddr,tokenIn,tokenOut,minReserveIn,amountIn ,amountOutMin] == self.showparams():
            self.logger.info(f'paramas already set')
            return {}
        func = self.contract.functions.setparams(_minReserveIn=minReserveIn, _amountIn=amountIn,  _amountOutMin=amountOutMin,  _tokenIn=tokenIn,  _tokenOut=tokenOut,  _pairaddr=pairaddr, _uniRouter=uniRouter,  _toaddr=toaddr)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def withdrawalltoken(self, token_address):
        gas = 200000
        token_address = self.chain.w3.toChecksumAddress(token_address)
        token_c = ERC20Contract(chain=self.chain, token_addr=token_address)
        if token_c.token_balance(self.address) > 0:
            func = self.contract.functions.withdrawalltoken(token_address)
            tx_param = self._build_tx(func, gas=gas)
            return tx_param
        else:
            return {}

    def withdrawparttoken(self, token_address, amount):
        gas = 200000
        token_address = self.chain.w3.toChecksumAddress(token_address)
        amount = int(amount)
        func = self.contract.functions.withdrawparttoken(token_address, amount)
        tx_param = self._build_tx(func, gas=gas)
        return tx_param

    def withdrawallcoin(self):
        gas = 200000
        if self.balance() > 0:
            func = self.contract.functions.withdraw2coin()
            tx_param = self._build_tx(func, gas=gas)
            return tx_param
        else:
            return {}
