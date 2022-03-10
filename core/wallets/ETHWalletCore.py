from decimal import Decimal

import ecdsa
import eth_abi

from core.libs import get_logger
from wconfig import CHAIN_ID, chain_token_addr
from .lib import cryptos

logger = get_logger('wallet_log.log')

try:
    import sha3
except:
    raise Exception("Requires PySHA3 : pip3 install pysha3")


class ETHwalletCore:
    def __init__(self, pubkey, network, api):
        self.pubkey = pubkey
        PKH = bytes.fromhex(cryptos.decompress(pubkey))
        self.Qpub = cryptos.decode_pubkey(pubkey)
        self.address = sha3.keccak_256(PKH[1:]).hexdigest()[-40:]
        self.api = api
        self.network = network

    def getbalance(self):
        return self.api.get_balance(self.address, 0)

    def getnonce(self):
        numtx = self.api.get_tx_num(self.address, "pending")
        return numtx

    def prepare(self, toaddr, paymentvalue, gprice, glimit):
        ## check balance
        balance = self.getbalance()
        maxspendable = balance - (gprice * glimit)
        if paymentvalue > maxspendable:
            raise Exception("Not enough fund for the tx")

        self.nonce = int2bytearray(self.getnonce())
        self.gasprice = int2bytearray(gprice)
        self.startgas = int2bytearray(glimit)
        self.to = bytearray.fromhex(toaddr)
        self.value = int2bytearray(int(paymentvalue))
        self.data = bytearray(b"")
        self.chainID = CHAIN_ID[self.network]

        v = int2bytearray(self.chainID)
        r = int2bytearray(0)
        s = int2bytearray(0)
        signing_tx = rlp_encode(
            [self.nonce, self.gasprice, self.startgas, self.to, self.value, self.data, v, r, s]
        )
        self.datahash = sha3.keccak_256(signing_tx).digest()
        return self.datahash

    def prepare_erc20(self, toaddr, paymentvalue, gprice, glimit, token):
        ## check balance
        # balance = self.getbalance()
        # maxspendable = balance - (gprice * glimit)
        # if paymentvalue > maxspendable:
        #     raise Exception("Not enough fund for the tx")
        if not chain_token_addr.get(token):
            raise Exception("Token isnot vailable")

        self.nonce = int2bytearray(self.getnonce())
        self.gasprice = int2bytearray(gprice)
        self.startgas = int2bytearray(glimit)
        contract_address = chain_token_addr.get(token)["contract_addr"]
        if contract_address.startswith("0x"):
            contract_address = chain_token_addr.get(token)["contract_addr"][2:]
        self.to = bytearray.fromhex(contract_address)
        self.value = int2bytearray(int(paymentvalue))
        # self.data = bytearray(b"")
        if not toaddr.startswith("0x"):
            toaddr = '0x' + toaddr
        transfer_param_abi = eth_abi.encode_abi(
            ['address', 'uint256'], [toaddr, int(Decimal(paymentvalue) * Decimal(
                10 ** int(chain_token_addr.get(token)["decimals"])))])  #
        # transfer
        self.data = bytearray.fromhex('a9059cbb') + transfer_param_abi
        # approval self.data = bytearray.fromhex('095ea7b3') + transfer_param_abi

        self.chainID = CHAIN_ID[self.network]

        v = int2bytearray(self.chainID)
        r = int2bytearray(0)
        s = int2bytearray(0)
        signing_tx = rlp_encode(
            [self.nonce, self.gasprice, self.startgas, self.to, self.value, self.data, v, r, s]
        )
        self.datahash = sha3.keccak_256(signing_tx).digest()
        return self.datahash

    def send(self, signature_der):
        # Signature decoding
        lenr = int(signature_der[3])
        lens = int(signature_der[5 + lenr])
        r = int.from_bytes(signature_der[4: lenr + 4], "big")
        s = int.from_bytes(signature_der[lenr + 6: lenr + 6 + lens], "big")
        # Parity recovery
        Q = ecdsa.keys.VerifyingKey.from_public_key_recovery_with_digest(
            signature_der, self.datahash, ecdsa.curves.SECP256k1, sigdecode=ecdsa.util.sigdecode_der
        )[1]
        if Q.to_string("uncompressed") == cryptos.encode_pubkey(self.Qpub, "bin"):
            i = 36
        else:
            i = 35
        # Signature encoding
        v = int2bytearray(2 * self.chainID + i)
        r = int2bytearray(r)
        s = int2bytearray(s)
        tx_final = rlp_encode(
            [self.nonce, self.gasprice, self.startgas, self.to, self.value, self.data, v, r, s]
        )
        txhex = tx_final.hex()
        logger.info(txhex)
        txid = self.api.pushtx(txhex)
        logger.info("DONE, txID : " + txid)
        return txid


def rlp_encode(input):
    if isinstance(input, bytearray):
        if len(input) == 1 and input[0] == 0:
            return bytearray(b"\x80")
        if len(input) == 1 and input[0] < 0x80:
            return input
        else:
            return encode_length(len(input), 0x80) + input
    elif isinstance(input, list):
        output = bytearray([])
        for item in input:
            output += rlp_encode(item)
        return encode_length(len(output), 0xC0) + output
    raise Exception("Bad input type, list or bytearray needed")


def encode_length(L, offset):
    if L < 56:
        return bytearray([L + offset])
    BL = to_binary(L)
    return bytearray([len(BL) + offset + 55]) + BL


def to_binary(x):
    if x == 0:
        return bytearray([])
    else:
        return to_binary(int(x // 256)) + bytearray([x % 256])


def int2bytearray(i):
    barr = (i).to_bytes(32, byteorder="big")
    while barr[0] == 0 and len(barr) > 1:
        barr = barr[1:]
    return bytearray(barr)
