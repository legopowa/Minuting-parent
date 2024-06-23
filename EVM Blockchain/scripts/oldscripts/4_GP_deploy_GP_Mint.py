import lorem

import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import network, web3, accounts, Wei, AnonIDContract, LamportBase2, Contract
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
from eth_utils import encode_hex #, encode
from eth_abi import encode, encode
from Crypto.Hash import keccak
from typing import List
import json
import os
import ast
import time
from time import sleep
import re
from typing import List
import struct
from offchain.local_functions import get_pkh_list
from offchain.KeyTracker_ import KeyTracker
from offchain.soliditypack import solidity_pack_value_bytes, solidity_pack_value, pack_keys, encode_packed_2d_list, solidity_pack_bytes, encode_packed, solidity_pack_pairs, solidity_pack, solidity_pack_bytes, solidity_pack_array
from offchain.Types import LamportKeyPair, Sig, PubPair
from offchain.functions import hash_b, sign_hash, verify_signed_hash
from eth_abi import encode, encode
from binascii import crc32, hexlify
import binascii
from offchain.crc import compute_crc
#from offchain.oracle_functions import extract_data_from_file, get_pkh_list, send_pkh_with_crc, save_received_data, read_till_eof, send_packed_file
import offchain.data_temp

SOF = b'\x01'  # Start Of File marker
EOF = b'\x04'  # End Of File marker
CRC_START = b'<CRC>'
CRC_END = b'</CRC>'



gas_strategy = LinearScalingStrategy("120 gwei", "1200 gwei", 1.1)

# if network.show_active() == "development":
gas_price(gas_strategy)

# ITERATIONS = 3

# def compute_crc(self, data: str) -> int:
#     return crc32(data.encode())

offchain.data_temp.received_data = b''

def encode_packed(*args):
    return b"".join([struct.pack(f"<{len(arg)}s", arg) for arg in args])


def custom_encode_packed(address, integer):
    # Convert the address to bytes and pad with zeroes
    address_bytes = bytes(Web3.toBytes(hexstr=address))

    # Convert the integer to bytes and pad with zeroes
    integer_bytes = encode('uint', integer)

    # Concatenate everything together
    result = address_bytes + b'\0' * 12 + integer_bytes + b'\0' * 12

    return result.decode('unicode_escape')

def main():
    for _ in range(1):  # This will repeat the whole logic 3 times
        lamport_test = LamportTest()
        
        # Convert all account objects to strings before passing them
        lamport_test.can_test_key_functions([str(acc) for acc in accounts])


oracle_pkh = []
master_pkh_1 = []
master_pkh_2 = []
master_pkh_3 = []
master_pkh_4 = []
arg1 = "GPGrens"
arg2 = "GPG"

# ABI encode the arguments
encoded_args = encode(['string', 'string'], [arg1, arg2])

# Load the bytecode of the contract (replace with actual bytecode)
full_bytecode = "0x608060405234801561001057600080fd5b50600080546001600160a01b03191673b3830ae69ee5962355e84f6bbac274ff337960e517905560408051808201909152600781526647504772656e7360c81b602082015260059061006290826102ad565b5060408051808201909152600381526247504760e81b602082015260069061008a90826102ad565b50610093610098565b6104a5565b600780546001600160a01b03191673f3a99a9a2836a6fcfceb846161b900b3d14472361790556100fe73239fa7623354ec26520de878b52f13fe84b069716100de601290565b6100ec9060ff16600a610468565b6100f9906201388061047b565b610126565b600780546001600160a01b031916732bcffac2b9eb65c7965008aab7228e455d81454a179055565b6007546001600160a01b031633146101845760405162461bcd60e51b815260206004820152601c60248201527f47505f4d696e743a20556e617574686f72697a6564206d696e74657200000000604482015260640160405180910390fd5b80600460008282546101969190610492565b90915550506001600160a01b038216600090815260016020526040812080548392906101c3908490610492565b90915550506040518181526001600160a01b0383169033907f9d228d69b5fdb8d273a2336f8fb8612d039631024ea9bf09c424a9503aa078f09060200160405180910390a35050565b634e487b7160e01b600052604160045260246000fd5b600181811c9082168061023657607f821691505b60208210810361025657634e487b7160e01b600052602260045260246000fd5b50919050565b601f8211156102a8576000816000526020600020601f850160051c810160208610156102855750805b601f850160051c820191505b818110156102a457828155600101610291565b5050505b505050565b81516001600160401b038111156102c6576102c661020c565b6102da816102d48454610222565b8461025c565b602080601f83116001811461030f57600084156102f75750858301515b600019600386901b1c1916600185901b1785556102a4565b600085815260208120601f198616915b8281101561033e5788860151825594840194600190910190840161031f565b508582101561035c5787850151600019600388901b60f8161c191681555b5050505050600190811b01905550565b634e487b7160e01b600052601160045260246000fd5b600181815b808511156103bd5781600019048211156103a3576103a361036c565b808516156103b057918102915b93841c9390800290610387565b509250929050565b6000826103d457506001610462565b816103e157506000610462565b81600181146103f757600281146104015761041d565b6001915050610462565b60ff8411156104125761041261036c565b50506001821b610462565b5060208310610133831016604e8410600b8410161715610440575081810a610462565b61044a8383610382565b806000190482111561045e5761045e61036c565b0290505b92915050565b600061047483836103c5565b9392505050565b80820281158282048414176104625761046261036c565b808201808211156104625761046261036c565b611400806104b46000396000f3fe608060405234801561001057600080fd5b50600436106101005760003560e01c80638486e2ff11610097578063e2eb6dab11610066578063e2eb6dab1461024a578063e5f855b71461025b578063e951ae231461026e578063f0dda65c1461028157600080fd5b80638486e2ff146101e357806395d89b41146101f6578063a9059cbb146101fe578063dd62ed3e1461021157600080fd5b80632a663120116100d35780632a6631201461016b578063313ce5671461018057806356bf7b571461018f57806370a08231146101ba57600080fd5b806306fdde0314610105578063095ea7b31461012357806318160ddd1461014657806323b872dd14610158575b600080fd5b61010d610294565b60405161011a9190610ecd565b60405180910390f35b610136610131366004610f03565b610326565b604051901515815260200161011a565b6004545b60405190815260200161011a565b610136610166366004610f2d565b6103f4565b61017e610179366004610f8d565b6105c3565b005b6040516012815260200161011a565b6000546101a2906001600160a01b031681565b6040516001600160a01b03909116815260200161011a565b61014a6101c8366004610ffa565b6001600160a01b031660009081526001602052604090205490565b61017e6101f1366004611015565b6106b9565b61010d6108fb565b61013661020c366004610f03565b61090a565b61014a61021f366004611070565b6001600160a01b03918216600090815260026020908152604080832093909416825291909152205490565b6007546001600160a01b03166101a2565b61017e610269366004611015565b6109ef565b61017e61027c366004610f8d565b610ae1565b61017e61028f366004610f03565b610d3d565b6060600580546102a3906110a3565b80601f01602080910402602001604051908101604052809291908181526020018280546102cf906110a3565b801561031c5780601f106102f15761010080835404028352916020019161031c565b820191906000526020600020905b8154815290600101906020018083116102ff57829003601f168201915b5050505050905090565b60006001600160a01b03831661038e5760405162461bcd60e51b815260206004820152602260248201527f45524332303a20617070726f766520746f20746865207a65726f206164647265604482015261737360f01b60648201526084015b60405180910390fd5b3360008181526002602090815260408083206001600160a01b03881680855290835292819020869055518581529192917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92591015b60405180910390a35060015b92915050565b60006001600160a01b03831661041c5760405162461bcd60e51b8152600401610385906110dd565b6001600160a01b0384166000908152600160205260409020548211156104545760405162461bcd60e51b815260040161038590611120565b6001600160a01b03841660009081526002602090815260408083203384529091529020548211156104d85760405162461bcd60e51b815260206004820152602860248201527f45524332303a207472616e7366657220616d6f756e74206578636565647320616044820152676c6c6f77616e636560c01b6064820152608401610385565b6001600160a01b0384166000908152600160205260408120805484929061050090849061117c565b90915550506001600160a01b0383166000908152600160205260408120805484929061052d90849061118f565b90915550506001600160a01b03841660009081526002602090815260408083203384529091528120805484929061056590849061117c565b92505081905550826001600160a01b0316846001600160a01b03167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040516105b191815260200190565b60405180910390a35060019392505050565b6000816040516020016105d691906111a2565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f61119061061f9089908990899088906004016111e8565b6020604051808303816000875af115801561063e573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061066291906112c9565b9050806106815760405162461bcd60e51b8152600401610385906112eb565b505060039190915533600090815260086020526040902080546001600160a01b0319166001600160a01b039092169190911790555050565b6000836040516020016106cc919061132c565b60405160208183030381529060405280519060200120905060035481036107055760405162461bcd60e51b815260040161038590611363565b600754604051600091610726916001600160a01b03909116906020016111a2565b60408051601f19818403018152918152336000908152600860205220549091506001600160a01b0316156107a85760405162461bcd60e51b815260206004820152602360248201527f47505f4d696e743a204e6f206d696e7465722072656d6f76616c2070726f706f6044820152621cd95960ea1b6064820152608401610385565b6007546001600160a01b03166107f95760405162461bcd60e51b815260206004820152601660248201527511d417d35a5b9d0e88139bc81b5a5b9d195c881cd95d60521b6044820152606401610385565b6000805460405163333f611160e01b81526001600160a01b039091169063333f6111906108309089908990899088906004016111e8565b6020604051808303816000875af115801561084f573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061087391906112c9565b9050806108925760405162461bcd60e51b8152600401610385906112eb565b6007546040516001600160a01b03909116907fc6711413797b8a562634e98c95d50e7619d39702ed5b82ce335dc93546c3a88c90600090a25050600780546001600160a01b03199081169091553360009081526008602052604090208054909116905550505050565b6060600680546102a3906110a3565b60006001600160a01b0383166109325760405162461bcd60e51b8152600401610385906110dd565b336000908152600160205260409020548211156109615760405162461bcd60e51b815260040161038590611120565b336000908152600160205260408120805484929061098090849061117c565b90915550506001600160a01b038316600090815260016020526040812080548492906109ad90849061118f565b90915550506040518281526001600160a01b0384169033907fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef906020016103e2565b600754604051600091610a10916001600160a01b03909116906020016111a2565b60408051601f19818403018152908290526000805463333f611160e01b8452919350916001600160a01b039091169063333f611190610a599088908890889088906004016111e8565b6020604051808303816000875af1158015610a78573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610a9c91906112c9565b905080610abb5760405162461bcd60e51b8152600401610385906112eb565b5050600355505033600090815260086020526040902080546001600160a01b0319169055565b600084604051602001610af4919061132c565b6040516020818303038152906040528051906020012090506003548103610b2d5760405162461bcd60e51b815260040161038590611363565b600082604051602001610b4091906111a2565b60408051808303601f19018152918152336000908152600860205220549091506001600160a01b03848116911614610bba5760405162461bcd60e51b815260206004820181905260248201527f4d7945524332303a204d696e7465722061646472657373206d69736d617463686044820152606401610385565b6007546001600160a01b03161580610bdf57506007546001600160a01b038481169116145b610c375760405162461bcd60e51b815260206004820152602360248201527f4d7945524332303a20416e6f74686572206d696e74657220616c7265616479206044820152621cd95d60ea1b6064820152608401610385565b6000805460405163333f611160e01b81526001600160a01b039091169063333f611190610c6e908a908a908a9088906004016111e8565b6020604051808303816000875af1158015610c8d573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610cb191906112c9565b905080610cd05760405162461bcd60e51b8152600401610385906112eb565b600780546001600160a01b0319166001600160a01b0386169081179091556040517ffe7c7fcb0ae0ce6bfd0a653fa3ab6c97a51a0819e6c27cdab8a08d456338c5fa90600090a2505033600090815260086020526040902080546001600160a01b03191690555050505050565b6007546001600160a01b03163314610d975760405162461bcd60e51b815260206004820152601c60248201527f47505f4d696e743a20556e617574686f72697a6564206d696e746572000000006044820152606401610385565b610da18282610da5565b5050565b6007546001600160a01b03163314610dff5760405162461bcd60e51b815260206004820152601c60248201527f47505f4d696e743a20556e617574686f72697a6564206d696e746572000000006044820152606401610385565b8060046000828254610e11919061118f565b90915550506001600160a01b03821660009081526001602052604081208054839290610e3e90849061118f565b90915550506040518181526001600160a01b0383169033907f9d228d69b5fdb8d273a2336f8fb8612d039631024ea9bf09c424a9503aa078f09060200160405180910390a35050565b6000815180845260005b81811015610ead57602081850181015186830182015201610e91565b506000602082860101526020601f19601f83011685010191505092915050565b602081526000610ee06020830184610e87565b9392505050565b80356001600160a01b0381168114610efe57600080fd5b919050565b60008060408385031215610f1657600080fd5b610f1f83610ee7565b946020939093013593505050565b600080600060608486031215610f4257600080fd5b610f4b84610ee7565b9250610f5960208501610ee7565b9150604084013590509250925092565b8061400081018310156103ee57600080fd5b8061200081018310156103ee57600080fd5b6000806000806140608587031215610fa457600080fd5b610fae8686610f69565b935061400085013567ffffffffffffffff811115610fcb57600080fd5b610fd787828801610f7b565b9350506140208501359150610fef6140408601610ee7565b905092959194509250565b60006020828403121561100c57600080fd5b610ee082610ee7565b6000806000614040848603121561102b57600080fd5b6110358585610f69565b925061400084013567ffffffffffffffff81111561105257600080fd5b61105e86828701610f7b565b92505061402084013590509250925092565b6000806040838503121561108357600080fd5b61108c83610ee7565b915061109a60208401610ee7565b90509250929050565b600181811c908216806110b757607f821691505b6020821081036110d757634e487b7160e01b600052602260045260246000fd5b50919050565b60208082526023908201527f45524332303a207472616e7366657220746f20746865207a65726f206164647260408201526265737360e81b606082015260800190565b60208082526026908201527f45524332303a207472616e7366657220616d6f756e7420657863656564732062604082015265616c616e636560d01b606082015260800190565b634e487b7160e01b600052601160045260246000fd5b818103818111156103ee576103ee611166565b808201808211156103ee576103ee611166565b60609190911b6bffffffffffffffffffffffff1916815260140190565b81835281816020850137506000828201602090810191909152601f909101601f19169091010190565b60006140608281018388845b610100811015611215576040808385379283019291909101906001016111f4565b50505061400084019190915261606083018660005b6101008110156112a15785830361405f190184528135368a9003601e1901811261125357600080fd5b8901602081810191359067ffffffffffffffff82111561127257600080fd5b81360383131561128157600080fd5b61128c8683856111bf565b9681019695509390930192505060010161122a565b5050856140208501528381036140408501526112bd8186610e87565b98975050505050505050565b6000602082840312156112db57600080fd5b81518015158114610ee057600080fd5b60208082526021908201527f4c616d706f7274426173653a20417574686f72697a6174696f6e206661696c656040820152601960fa1b606082015260800190565b60008183825b61010081101561135357604080838537928301929190910190600101611332565b5050506140008201905092915050565b60208082526041908201527f4c616d706f7274426173653a2043616e6e6f7420757365207468652073616d6560408201527f206b6579636861696e20747769636520666f7220746869732066756e6374696f6060820152603760f91b608082015260a0019056fea2646970667358221220e415ea1486e6c68870ba639badfd71c786cca264d6e7be37ff7ca77af65556bd64736f6c63430008190033"
#print(encoded_args.hex())
# Append the encoded arguments to the bytecode
#print(full_bytecode)
class LamportTest:
    
    def __init__(self):

        self.k1 = KeyTracker("master1") # new keys made here
        self.k2 = KeyTracker("master2")
        self.k3 = KeyTracker("oracle1")
        self.k4 = KeyTracker("master3")
        self.k5 = KeyTracker("master4")
        print("Initializing LamportTest...")
        with open('contract_AnonID.txt', 'r') as file:
            contract_address = file.read().strip()
        #print(contract_address)
        self.contract = AnonIDContract.at(contract_address)
        #lamport_base = LamportBase.at(contract_address) # <<< not working!
        accounts.default = str(accounts[0]) 
        # link it up
        pkhs = self.get_pkh_list(self.contract, 0)
        opkhs = self.get_pkh_list(self.contract, 1)
        # priv level set here with integer ^
        print("contract pkh", pkhs)

        self.load_four_masters(pkhs, "master")
        self.load_keys(opkhs, "oracle")
        print('init done')

    def get_pkh_list(self, contract, privilege_level):
        with open('contract_LamportBase2.txt', 'r') as file:
            contract_address = file.read().strip()
        contract2 = LamportBase2.at(contract_address)

        contract_pkh = str(contract2.getPKHsByPrivilege(privilege_level))
        # gonna need some kind of wait / delay here for primetime
        print(contract_pkh)
        contract_pkh_list = re.findall(r'0x[a-fA-F0-9]+', contract_pkh)
        pkh_list = [pkh for pkh in contract_pkh_list]  # Removing '0x' prefix
        contract_pkh_string = json.dumps(contract_pkh)
        contract_pkh_list = json.dumps(contract_pkh_string)
        return pkh_list

    
    def load_four_masters(self, pkhs, filename):
        pkh_index = 0
        master1_loaded = False
        master2_loaded = False
        master3_loaded = False
        master4_loaded = False
        global master_pkh_1
        global master_pkh_2
        global master_pkh_3
        global master_pkh_4

        while not master1_loaded and pkh_index < len(pkhs):
            try:
                self.k1.load(self, filename + '1', pkhs[pkh_index])
                print(f"Load successful for Master 1, PKH: {pkhs[pkh_index]}")
                master1_loaded = True
                key_tracker_1 = self.k1.current_key_pair()
                master_pkh_1 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 1, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master1_loaded:
            print("Load failed for all provided PKHs for Master 1")
            return

        while not master2_loaded and pkh_index < len(pkhs):
            try:
                self.k2.load(self, filename + '2', pkhs[pkh_index])
                print(f"Load successful for Master 2, PKH: {pkhs[pkh_index]}")
                master2_loaded = True
                key_tracker_2 = self.k2.current_key_pair()
                master_pkh_2 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 2, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master3_loaded:
            print("Load failed for all provided PKHs for Master 2")

        while not master3_loaded and pkh_index < len(pkhs):
            try:
                self.k4.load(self, filename + '3', pkhs[pkh_index])
                print(f"Load successful for Master 3, PKH: {pkhs[pkh_index]}")
                master3_loaded = True
                key_tracker_3 = self.k4.current_key_pair()
                master_pkh_3 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 3, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master4_loaded:
            print("Load failed for all provided PKHs for Master 2")

        while not master4_loaded and pkh_index < len(pkhs):
            try:
                self.k5.load(self, filename + '4', pkhs[pkh_index])
                print(f"Load successful for Master 3, PKH: {pkhs[pkh_index]}")
                master4_loaded = True
                key_tracker_4 = self.k5.current_key_pair()
                master_pkh_4 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Master 3, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not master4_loaded:
            print("Load failed for all provided PKHs for Master 2")            

    def load_keys(self, pkhs, filename):
        global oracle_pkh
        for pkh in pkhs:
            try:
                oracle_pkh = pkh
                self.k3.load(self, filename + '1', pkh)
                print(f"Load successful for PKH: {pkh}")
                return  # Exit function after successful load
            except InvalidAddress:
                print(f"No valid keys found for PKH: {pkh}")
                continue  # Try the next pkh if this one fails
        print("Load failed for all provided PKHs")

    def can_test_key_functions(self, accs):
        global master_pkh_1
        global master_pkh_2
        global master_pkh_3
        global master_pkh_4
        print("Running 'can_test_key_functions'...")
        with open('contract_AnonID.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = AnonIDContract.at(contract_address)
        print("Contract referenced.")
        print('master_pkh_3', master_pkh_3)
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        current_keys = self.k4.load(self, "master3", master_pkh_3)
        current_pkh = self.k4.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k4.get_next_key_pair()
        nextpkh = self.k4.pkh_from_public_key(next_keys.pub)
        #pairs = generate_address_value_pairs(10)
        #packed_pairs = solidity_pack_pairs(pairs)
        #_newCap = int(300000)
        #numToBroadcast = int(1000000)
        #pnumToBroadcast = numToBroadcast.to_bytes(4, 'big')
        #paddednumToBroadcast = solidity_pack_value_bytes(pnumToBroadcast)
        #paddressToBroadcast = '0x99a840C3BEEe41c3F5B682386f67277CfE3E3e29' # activity contract needing approval
        # with open('whitelist_contract.txt', 'r') as file:
        #     contract_address2 = file.read()
        #     contract_address2 = contract_address2.strip().replace('\n', '') 
        hashToBroadcast = Web3.keccak(hexstr=full_bytecode)
        print(hashToBroadcast.hex())
        packed_message = str.lower(hashToBroadcast.hex())[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        
        _contract.createContractStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            hashToBroadcast,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )
        self.k4.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_3 = nextpkh


        current_keys = self.k5.load(self, "master4", master_pkh_4)
        current_pkh = self.k5.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k5.get_next_key_pair()
        nextpkh = self.k5.pkh_from_public_key(next_keys.pub)
        #pairs = generate_address_value_pairs(10)
        #packed_pairs = solidity_pack_pairs(pairs)
        #_newCap = int(300000)
        #numToBroadcast = int(1000000)
        #pnumToBroadcast = numToBroadcast.to_bytes(4, 'big')
        #paddednumToBroadcast = solidity_pack_value_bytes(pnumToBroadcast)
        #paddressToBroadcast = '0x99a840C3BEEe41c3F5B682386f67277CfE3E3e29' # activity contract needing approval
        # with open('whitelist_contract.txt', 'r') as file:
        #     contract_address2 = file.read()
        #     contract_address2 = contract_address2.strip().replace('\n', '') 
        hashToBroadcast = Web3.keccak(hexstr=full_bytecode)
        print(hashToBroadcast.hex())
        packed_message = str.lower(hashToBroadcast.hex())[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        
        _contract.createContractStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            hashToBroadcast,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )
        self.k5.save(trim = False)
        #self.k4.save(trim = False)
        master_pkh_4 = nextpkh

        #current_keys = self.k2.load(self, "master2", master_pkh_2)
        #next_keys = self.k2.get_next_key_pair()
        #nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        #paddressToBroadcast = '0xfd003CA44BbF4E9fB0b2fF1a33fc2F05A6C2EFF9'

        #packed_message = str.lower(full_bytecode)[2:].encode() + nextpkh[2:].encode()

        #callhash = hash_b(str(packed_message.decode()))
        #sig = sign_hash(callhash, current_keys.pri) 


        
        tx = _contract.createContractStepThree(

            full_bytecode,
            {'from': brownie_account, 'gas_limit': 3999999}    
        )
        tx.wait(1)

        # Extract the new contract address from the transaction's events
        new_contract_address = tx.events['ContractCreated']['contractAddress']

        print(f"New contract address: {new_contract_address}")
        #self.k2.save(trim = False)

        with open('contract_GP_Mint-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()