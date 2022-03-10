import json
import time
import urllib.parse
import urllib.request

from wconfig import CHAIN_API_URL


class etherscan_api:
    def __init__(self, api_key, network):
        self.apikey = api_key
        self.network = network
        # https://api.etherscan.io/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey=YourApiKeyToken
        if self.network == "test":
            self.url = "https://api.hecoinfo.com/api"
        else:
            self.url = CHAIN_API_URL[self.network]
        self.params = {"token": self.apikey}
        self.params = {}
        self.jsres = []

    def getData(self, parameters={}):
        parameters.update(self.params)
        params_enc = urllib.parse.urlencode(parameters)
        # data = {"jsonrpc":"2.0","method":method,"params":params ,"id":1}
        try:
            # Enforce 5s per query without apikey
            time.sleep(1)
            req = urllib.request.Request(
                self.url + "?" + params_enc,
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                # data = json.dumps(data).encode('utf-8')
            )
            self.webrsc = urllib.request.urlopen(req)
            self.jsres = json.load(self.webrsc)
        except Exception as ex:
            raise IOError(
                "Error while processing request:\n%s"
                % (self.url + "->" + parameters + " : " + str(self.params))
            )

    def checkapiresp(self):
        if "error" in self.jsres:
            print(" !! ERROR :")
            raise Exception(self.jsres["error"])
        if "errors" in self.jsres:
            print(" !! ERRORS :")
            raise Exception(self.jsres["errors"])

    def get_balance(self, addr, nconf):  # nconf 0 or 1
        # if nconf==0: datap = "pending"
        # if nconf==1: datap = "latest"
        self.getData({"module": "account", "action": "balance", "address": "0x" + addr})
        balraw = self.getKey("result")
        if balraw == []:
            return 0
        balance = int(balraw)
        return balance

    def pushtx(self, txhex):
        self.getData({"module": "proxy", "action": "eth_sendRawTransaction", "hex": "0x" + txhex})
        self.checkapiresp()
        return self.getKey("result")

    def get_tx_num(self, addr, blocks):
        self.getData(
            {"module": "proxy", "action": "eth_getTransactionCount", "address": "0x" + addr}
        )
        self.checkapiresp()
        return int(self.getKey("result")[2:], 16)

    def get_fee(self, priority):
        raise Exception("Not yet implemented for this API")

    def getKey(self, keychar):
        out = self.jsres
        path = keychar.split("/")
        for key in path:
            if key.isdigit():
                key = int(key)
            try:
                out = out[key]
            except:
                out = []
        return out
