from hdwallet import HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.utils import generate_mnemonic

from core.eoa_account import EoaAccount


class EthAddressDB:
    def __init__(self, MNEMONIC):
        self.MNEMONIC = MNEMONIC
        # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
        self.LANGUAGE: str = "english"  # Default is english

        # Choose strength 128, 160, 192, 224 or 256
        self.STRENGTH: int = 128  # Default is 128

        # Initialize Ethereum mainnet HDWallet
        self.hdwallet: HDWallet = HDWallet(cryptocurrency=EthereumMainnet)
        # Get Ethereum HDWallet from mnemonic
        self.hdwallet.from_mnemonic(
            mnemonic=MNEMONIC, passphrase=None, language=self.LANGUAGE
        )

    def generate_mnemonic(self):

        # Generate new mnemonic words
        self.MNEMONIC: str = generate_mnemonic(language=self.LANGUAGE, strength=self.STRENGTH)
        print(self.MNEMONIC)
        # return MNEMONIC

    # def generate_wallet(self):
    #     # Secret passphrase for mnemonic
    #     PASSPHRASE: Optional[str] = None  # "meherett"
    #
    #     # Initialize Ethereum mainnet HDWallet
    #     self.hdwallet: HDWallet = HDWallet(cryptocurrency=EthereumMainnet)
    #     # Get Ethereum HDWallet from mnemonic
    #     self.hdwallet.from_mnemonic(
    #         mnemonic=MNEMONIC, passphrase=PASSPHRASE, language=self.LANGUAGE
    #     )
    #
    #     print("Mnemonic:", self.hdwallet.mnemonic())
    #     print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")

    def print_all_addr(self):
        # Get Ethereum HDWallet information's from address indexes
        for address_index in range(100):
            # Derivation from Ethereum BIP44 path
            self.hdwallet.from_path(
                path=EthereumMainnet.BIP44_PATH.format(
                    account=0, change=0, address=address_index
                )
            )
            # Print address_index, path, address and private_key
            print(
                f"HDWallet: ({address_index}) {self.hdwallet.path()} {self.hdwallet.address()} 0x{self.hdwallet.private_key()}")
            # Clean derivation indexes/path
            self.hdwallet.clean_derivation()

    def print_addr_lst(self, range_start, range_end):
        # Get Ethereum HDWallet information's from address indexes
        lst = []
        for address_index in range(range_start, range_end):
            # Derivation from Ethereum BIP44 path
            self.hdwallet.from_path(
                path=EthereumMainnet.BIP44_PATH.format(
                    account=0, change=0, address=address_index
                )
            )
            # Print address_index, path, address and private_key
            print(
                f"HDWallet: ({address_index}) {self.hdwallet.path()} {self.hdwallet.address()} 0x{self.hdwallet.private_key()}")
            lst.append(self.hdwallet.address())
            # Clean derivation indexes/path
            self.hdwallet.clean_derivation()
        return lst

    def get_hd_address(self, address_index):
        self.hdwallet.from_path(
            path=EthereumMainnet.BIP44_PATH.format(
                account=0, change=0, address=address_index
            )
        )
        addr = self.hdwallet.address()
        #print(f"HDWallet: ({address_index}) {self.hdwallet.path()} {addr}  ")

        self.hdwallet.clean_derivation()
        return addr

    def get_hd_privatekey(self, address_index):
        self.hdwallet.from_path(
            path=EthereumMainnet.BIP44_PATH.format(
                account=0, change=0, address=address_index
            )
        )
        # print(f"({address_index}) {self.hdwallet.path()} {self.hdwallet.address()} 0x{self.hdwallet.private_key()}")

        private_key = "0x" + self.hdwallet.private_key()
        self.hdwallet.clean_derivation()
        return private_key

    def get_eoa_account(self, address_index):
        return EoaAccount(self.get_hd_address(address_index), self.get_hd_privatekey(address_index))


if __name__ == "__main__":
    w = EthAddressDB()
    w.generate_wallet()
    w.print_all_addr()
    print(w.get_hd_address(1))
    print(w.get_hd_privatekey(1))
