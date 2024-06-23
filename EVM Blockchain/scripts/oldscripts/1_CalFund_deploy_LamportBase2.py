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
full_bytecode = "0x60806040526000805460ff1916905534801561001a57600080fd5b5061004660007fb7b18ded9664d1a8e923a5942ec1ca5cd8c13c40eb1a5215d5800600f5a587be6100ae565b61007160007f1ed304ab73e124b0b99406dfa1388a492a818837b4b41ce5693ad84dacfc3f256100ae565b61009c60017fd62569e61a6423c880a429676be48756c931fe0519121684f5fb05cbd17877fa6100ae565b6000805460ff19166001179055610209565b600060405180604001604052808460028111156100cd576100cd6101c7565b81526020018390526001805480820182556000829052825160029182027fb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6018054949550859490939192849260ff1990921691908490811115610132576101326101c7565b021790555060209182015160019182015560008481526002928390526040902083518154859492939192849260ff1990921691908490811115610177576101776101c7565b0217905550602082015181600101559050507f2172c7b01a6de957d29fd6166a23025d181bf56538ad606a526ab2d62603f3fc83836040516101ba9291906101dd565b60405180910390a1505050565b634e487b7160e01b600052602160045260246000fd5b60408101600384106101ff57634e487b7160e01b600052602160045260246000fd5b9281526020015290565b61231a806102186000396000f3fe608060405234801561001057600080fd5b506004361061010b5760003560e01c8063a543c59f116100a2578063b97b4f7711610071578063b97b4f7714610227578063b9d57c5f14610247578063bc60fb4914610269578063bd5a6d071461027c578063e1daa9531461028f57600080fd5b8063a543c59f146101d4578063a9711ee3146101e7578063af82f3e714610214578063b4314f63146101d457600080fd5b80634a89d52b116100de5780634a89d52b146101845780634bdd44991461019757806354f9ee03146101ae5780635796841a146101c157600080fd5b80630cb6aaf114610110578063251de3901461013a5780632fd5c2471461014f578063333f611114610171575b600080fd5b61012361011e366004611d05565b6102a2565b604051610131929190611d56565b60405180910390f35b61014d610148366004611d9b565b6102d4565b005b60005461016190610100900460ff1681565b6040519015158152602001610131565b61016161017f366004611e14565b6104d1565b610161610192366004611e14565b6105c2565b6101a060065481565b604051908152602001610131565b61014d6101bc366004611d9b565b610619565b61014d6101cf366004611d9b565b6107c1565b61014d6101e2366004611d9b565b6109c8565b6101236101f5366004611d05565b6002602052600090815260409020805460019091015460ff9091169082565b610161610222366004611f09565b610b6b565b61023a610235366004611f62565b610c20565b6040516101319190611f83565b61025a610255366004611d05565b610dbc565b60405161013193929190611fc7565b61014d610277366004611d9b565b610eb0565b61014d61028a366004611d9b565b611396565b61014d61029d366004611d9b565b611861565b600181815481106102b257600080fd5b60009182526020909120600290910201805460019091015460ff909116915082565b838383836040516020016102ea91815260200190565b60408051601f1981840301815291905260005460ff166103255760405162461bcd60e51b815260040161031c90611fe6565b60405180910390fd5b600084604051602001610338919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff169081111561037857610378611d1e565b146103955760405162461bcd60e51b815260040161031c90612054565b600082846040516020016103aa92919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a160006103ee828789610b6b565b6000805461ff0019166101008315150217905590508061047257604051828152600080516020612285833981519152906020015b60405180910390a160405162461bcd60e51b815260206004820181905260248201527f4c616d706f7274426173653a20566572696669636174696f6e206661696c6564604482015260640161031c565b600083815260026020526040908190205490516000805160206122c5833981519152916104a89160ff9091169086908990611fc7565b60405180910390a16104ba8386611a54565b505050600394909455505050600591909155505050565b6000805460ff166104f45760405162461bcd60e51b815260040161031c90611fe6565b600085604051602001610507919061201d565b60408051601f198184030181529190528051602090910120905060005b60008281526002602081905260409091205460ff169081111561054957610549611d1e565b146105585760009150506105ba565b6000838560405160200161056d92919061208b565b6040516020818303038152906040528051906020012060001c9050600061059582888a610b6b565b9050806105a857600093505050506105ba565b6105b28387611a54565b600193505050505b949350505050565b6000805460ff166105e55760405162461bcd60e51b815260040161031c90611fe6565b6000856040516020016105f8919061201d565b60408051601f19818403018152919052805160209091012090506001610524565b8383838360405160200161062f91815260200190565b60408051601f1981840301815291905260005460ff166106615760405162461bcd60e51b815260040161031c90611fe6565b600084604051602001610674919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff16908111156106b4576106b4611d1e565b146106d15760405162461bcd60e51b815260040161031c90612054565b600082846040516020016106e692919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a1600061072a828789610b6b565b6000805461ff001916610100831515021790559050806107625760405182815260008051602061228583398151915290602001610422565b600083815260026020526040908190205490516000805160206122c5833981519152916107989160ff9091169086908990611fc7565b60405180910390a16107aa8386611a54565b505050600494909455505050600591909155505050565b838383836040516020016107d791815260200190565b60408051601f1981840301815291905260005460ff166108095760405162461bcd60e51b815260040161031c90611fe6565b60008460405160200161081c919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff169081111561085c5761085c611d1e565b146108795760405162461bcd60e51b815260040161031c90612054565b6000828460405160200161088e92919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a160006108d2828789610b6b565b6000805461ff0019166101008315150217905590508061090a5760405182815260008051602061228583398151915290602001610422565b600083815260026020526040908190205490516000805160206122c5833981519152916109409160ff9091169086908990611fc7565b60405180910390a16109528386611a54565b60008b604051602001610965919061201d565b60408051601f198184030181529190528051602090910120600680546000909155909150811415806109a95760405162461bcd60e51b815260040161031c906120bd565b6109b460008b611bf9565b505060006006555050505050505050505050565b838383836040516020016109de91815260200190565b60408051601f1981840301815291905260005460ff16610a105760405162461bcd60e51b815260040161031c90611fe6565b600084604051602001610a23919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff1690811115610a6357610a63611d1e565b14610a805760405162461bcd60e51b815260040161031c90612054565b60008284604051602001610a9592919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a16000610ad9828789610b6b565b6000805461ff00191661010083151502179055905080610b115760405182815260008051602061228583398151915290602001610422565b600083815260026020526040908190205490516000805160206122c583398151915291610b479160ff9091169086908990611fc7565b60405180910390a1610b598386611a54565b50505060069590955550505050505050565b6000805b610100811015610c135783816101008110610b8c57610b8c61211b565b602002810190610b9c9190612131565b604051610baa92919061217f565b604051809103902083826101008110610bc557610bc561211b565b6040020160008360ff036001901b881611610be1576000610be4565b60015b60ff1660028110610bf757610bf761211b565b602002013514610c0b576000915050610c19565b600101610b6f565b50600190505b9392505050565b60015460609060009067ffffffffffffffff811115610c4157610c41611dfe565b604051908082528060200260200182016040528015610c6a578160200160208202803683370190505b5090506000805b600154811015610d2157846002811115610c8d57610c8d611d1e565b60018281548110610ca057610ca061211b565b600091825260209091206002918202015460ff1690811115610cc457610cc4611d1e565b03610d195760018181548110610cdc57610cdc61211b565b906000526020600020906002020160010154838381518110610d0057610d0061211b565b602090810291909101015281610d158161218f565b9250505b600101610c71565b5060008167ffffffffffffffff811115610d3d57610d3d611dfe565b604051908082528060200260200182016040528015610d66578160200160208202803683370190505b50905060005b82811015610db357838181518110610d8657610d8661211b565b6020026020010151828281518110610da057610da061211b565b6020908102919091010152600101610d6c565b50949350505050565b60008181526002602081905260408083208151808301909252805484938493849390929091839160ff1690811115610df657610df6611d1e565b6002811115610e0757610e07611d1e565b815260019190910154602091820152810151909150600003610e3b5760405162461bcd60e51b815260040161031c906121b6565b60005b600154811015610e90578560018281548110610e5c57610e5c61211b565b90600052602060002090600202016001015403610e885781516020909201519194509092509050610ea9565b600101610e3e565b5060405162461bcd60e51b815260040161031c906121b6565b9193909250565b83838383604051602001610ec691815260200190565b60408051601f1981840301815291905260005460ff16610ef85760405162461bcd60e51b815260040161031c90611fe6565b600084604051602001610f0b919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff1690811115610f4b57610f4b611d1e565b14610f685760405162461bcd60e51b815260040161031c90612054565b60008284604051602001610f7d92919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a16000610fc1828789610b6b565b6000805461ff00191661010083151502179055905080610ff95760405182815260008051602061228583398151915290602001610422565b600083815260026020526040908190205490516000805160206122c58339815191529161102f9160ff9091169086908990611fc7565b60405180910390a16110418386611a54565b60008b604051602001611054919061201d565b604051602081830303815290604052805190602001209050600554810361108d5760405162461bcd60e51b815260040161031c906121ed565b88600454146110de5760405162461bcd60e51b815260206004820152601e60248201527f4c616d706f7274426173653a204b65797320646f206e6f74206d617463680000604482015260640161031c565b600154891061112f5760405162461bcd60e51b815260206004820152601e60248201527f4c616d706f7274426173653a20496e76616c6964206b657920696e6465780000604482015260640161031c565b600060018a815481106111445761114461211b565b90600052602060002090600202016040518060400160405290816000820160009054906101000a900460ff16600281111561118157611181611d1e565b600281111561119257611192611d1e565b81526001919091015460209091015290506002815160028111156111b8576111b8611d1e565b036112055760405162461bcd60e51b815260206004820181905260248201527f4c616d706f7274426173653a204b657920616c72656164792064656c65746564604482015260640161031c565b8051604080514260208083019190915244828401528251808303840181526060909201909252805191012060018054630de1e7ed60e41b8318929183918f9081106112525761125261211b565b906000526020600020906002020160010181905550600260018e8154811061127c5761127c61211b565b906000526020600020906002020160000160006101000a81548160ff021916908360028111156112ae576112ae611d1e565b021790555060018d815481106112c6576112c661211b565b60009182526020808320858452600291829052604090932091810290920180548254919360ff90911691839160ff1990911690600190849081111561130d5761130d611d1e565b0217905550600191820154908201556020808601805160009081526002928390526040808220805460ff19168155909401555191517f0643be3612916977c69d5ed1abb75a50cca49df49ba2444d836e2a0cf65fe07492611372928792879190612254565b60405180910390a15050600060048190556005555050505050505050505050505050565b838383836040516020016113ac91815260200190565b60408051601f1981840301815291905260005460ff166113de5760405162461bcd60e51b815260040161031c90611fe6565b6000846040516020016113f1919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff169081111561143157611431611d1e565b1461144e5760405162461bcd60e51b815260040161031c90612054565b6000828460405160200161146392919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a160006114a7828789610b6b565b6000805461ff001916610100831515021790559050806114df5760405182815260008051602061228583398151915290602001610422565b600083815260026020526040908190205490516000805160206122c5833981519152916115159160ff9091169086908990611fc7565b60405180910390a16115278386611a54565b60008b60405160200161153a919061201d565b60405160208183030381529060405280519060200120905060055481036115735760405162461bcd60e51b815260040161031c906121ed565b88600354146115c45760405162461bcd60e51b815260206004820152601e60248201527f4c616d706f7274426173653a204b65797320646f206e6f74206d617463680000604482015260640161031c565b600554818a6000808481526002602081905260409091205460ff16908111156115ef576115ef611d1e565b14801561161d5750600082815260026020819052604082205460ff169081111561161b5761161b611d1e565b145b6116805760405162461bcd60e51b815260206004820152602e60248201527f4c616d706f7274426173653a2050726f7669646564206b65797320617265206e60448201526d6f74206d6173746572206b65797360901b606482015260840161031c565b8281141580156116905750818114155b6116f65760405162461bcd60e51b815260206004820152603160248201527f4c616d706f7274426173653a204d6173746572206b6579732063616e6e6f742060448201527064656c657465207468656d73656c76657360781b606482015260840161031c565b60008181526002602052604081206001015490036117625760405162461bcd60e51b815260206004820152602360248201527f4c616d706f7274426173653a204e6f2073756368206b6579202864656c6574696044820152626f6e2960e81b606482015260840161031c565b60005b6001548110156118455781600182815481106117835761178361211b565b9060005260206000209060020201600101540361183d57600082815260026020818152604080842080548251428186015244818501528351808203850181526060909101938490528051908501209588905292849052630de1e7ed60e41b85186001820181905560ff198416851790915560ff9092169391927f0643be3612916977c69d5ed1abb75a50cca49df49ba2444d836e2a0cf65fe0749161182d91869189918791612254565b60405180910390a1505050611845565b600101611765565b5050600060038190556005555050505050505050505050505050565b8383838360405160200161187791815260200190565b60408051601f1981840301815291905260005460ff166118a95760405162461bcd60e51b815260040161031c90611fe6565b6000846040516020016118bc919061201d565b60408051601f19818403018152919052805160209091012090506000808281526002602081905260409091205460ff16908111156118fc576118fc611d1e565b146119195760405162461bcd60e51b815260040161031c90612054565b6000828460405160200161192e92919061208b565b60408051601f1981840301815290829052805160209182012080835292506000805160206122a5833981519152910160405180910390a16000611972828789610b6b565b6000805461ff001916610100831515021790559050806119aa5760405182815260008051602061228583398151915290602001610422565b600083815260026020526040908190205490516000805160206122c5833981519152916119e09160ff9091169086908990611fc7565b60405180910390a16119f28386611a54565b60008b604051602001611a05919061201d565b60408051601f19818403018152919052805160209091012060068054600090915590915081141580611a495760405162461bcd60e51b815260040161031c906120bd565b6109b460018b611bf9565b6000828152600260205260408120600101549003611a845760405162461bcd60e51b815260040161031c906121b6565b604080518082018252600084815260026020819052928120549092829160ff1690811115611ab457611ab4611d1e565b8152602001838152509050806002600084815260200190815260200160002060008201518160000160006101000a81548160ff02191690836002811115611afd57611afd611d1e565b02179055506020918201516001918201556000858152600290925260408220805460ff19168155018190555b600154811015611bc9578360018281548110611b4757611b4761211b565b90600052602060002090600202016001015403611bc1578160018281548110611b7257611b7261211b565b906000526020600020906002020160008201518160000160006101000a81548160ff02191690836002811115611baa57611baa611d1e565b021790555060208201518160010155905050611bc9565b600101611b29565b5080516040516000805160206122c583398151915291611bec9186908690611fc7565b60405180910390a1505050565b60006040518060400160405280846002811115611c1857611c18611d1e565b81526020018390526001805480820182556000829052825160029182027fb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6018054949550859490939192849260ff1990921691908490811115611c7d57611c7d611d1e565b021790555060209182015160019182015560008481526002928390526040902083518154859492939192849260ff1990921691908490811115611cc257611cc2611d1e565b0217905550602082015181600101559050507f2172c7b01a6de957d29fd6166a23025d181bf56538ad606a526ab2d62603f3fc8383604051611bec929190611d56565b600060208284031215611d1757600080fd5b5035919050565b634e487b7160e01b600052602160045260246000fd5b60038110611d5257634e487b7160e01b600052602160045260246000fd5b9052565b60408101611d648285611d34565b8260208301529392505050565b806140008101831015611d8357600080fd5b92915050565b806120008101831015611d8357600080fd5b6000806000806140608587031215611db257600080fd5b611dbc8686611d71565b935061400085013567ffffffffffffffff811115611dd957600080fd5b611de587828801611d89565b9497949650505050614020830135926140400135919050565b634e487b7160e01b600052604160045260246000fd5b6000806000806140608587031215611e2b57600080fd5b611e358686611d71565b935061400085013567ffffffffffffffff80821115611e5357600080fd5b611e5f88838901611d89565b94506140208701359350614040870135915080821115611e7e57600080fd5b818701915087601f830112611e9257600080fd5b813581811115611ea457611ea4611dfe565b604051601f8201601f19908116603f01168101908382118183101715611ecc57611ecc611dfe565b816040528281528a6020848701011115611ee557600080fd5b82602086016020830137600060208483010152809550505050505092959194509250565b60008060006140408486031215611f1f57600080fd5b83359250602084013567ffffffffffffffff811115611f3d57600080fd5b611f4986828701611d89565b925050611f598560408601611d71565b90509250925092565b600060208284031215611f7457600080fd5b813560038110610c1957600080fd5b6020808252825182820181905260009190848201906040850190845b81811015611fbb57835183529284019291840191600101611f9f565b50909695505050505050565b60608101611fd58286611d34565b602082019390935260400152919050565b6020808252601c908201527f4c616d706f7274426173653a206e6f7420696e697469616c697a656400000000604082015260600190565b60008183825b61010081101561204457604080838537928301929190910190600101612023565b5050506140008201905092915050565b6020808252601d908201527f4c616d706f7274426173653a204e6f742061206d6173746572206b6579000000604082015260600190565b6000835160005b818110156120ac5760208187018101518583015201612092565b509190910191825250602001919050565b602080825260409082018190527f4c616d706f7274426173653a20504b48206d617463686573206c617374207573908201527f656420504b482028757365207365706172617465207365636f6e64206b657929606082015260800190565b634e487b7160e01b600052603260045260246000fd5b6000808335601e1984360301811261214857600080fd5b83018035915067ffffffffffffffff82111561216357600080fd5b60200191503681900382131561217857600080fd5b9250929050565b8183823760009101908152919050565b6000600182016121af57634e487b7160e01b600052601160045260246000fd5b5060010190565b60208082526018908201527f4c616d706f7274426173653a204e6f2073756368206b65790000000000000000604082015260600190565b60208082526041908201527f4c616d706f7274426173653a2043616e6e6f7420757365207468652073616d6560408201527f206b6579636861696e20747769636520666f7220746869732066756e6374696f6060820152603760f91b608082015260a00190565b608081016122628287611d34565b84602083015283604083015261227b6060830184611d34565b9594505050505056fe32629d580208e19f97e5752eef849e102f803999c88aa7f75e12b1744eecd5a7d87e68f36f73a7eb22739d6639e36cafebfcde0b5543340b39f42cac68fdd1f06825a39bd161f4ef5aab6cfd2c26db3ee0005c11b43cffd544fc876312116edda2646970667358221220e241e3c6227a987c9bc72f1a36ff0d587e6561d4e9d2b6ff2bead84d7f6eae9c64736f6c63430008190033"
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

        with open('contract_LamportBase2-coin.txt', 'w') as file:
            # Write the contract address to the file
            file.write(new_contract_address)
        exit()