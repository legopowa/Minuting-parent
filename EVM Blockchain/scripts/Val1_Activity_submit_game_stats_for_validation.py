import lorem
from pathlib import Path
import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import network, web3, accounts, Wei, GameValidator, LamportBase2, PlayerDatabase, Contract
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
from eth_utils import encode_hex #, encode
from eth_abi import encode
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
def compute_keccak_hash(serverPlayerLists):
    # Initialize Web3
    #w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Update with your provider

    # Convert the list of tuples into a format for hashing
    types_and_values = []
    for serverIP, playerNames in serverPlayerLists:
        types_and_values.append(('string', serverIP))
        # For dynamic arrays, prepend the length of the array followed by its items
        types_and_values.append(('uint256', len(playerNames)))  # Array length
        for playerName in playerNames:
            types_and_values.append(('string', playerName))  # Array items

    # Separate the types and values
    types = [pair[0] for pair in types_and_values]
    values = [pair[1] for pair in types_and_values]

    # Compute the keccak hash
    hash = w3.solidity_keccak(types, values)

    return hash.hex()

w3 = Web3()
def load_mnemonic(mnemonic_file):
    mnemonic_path = Path(mnemonic_file)
    if not mnemonic_path.is_file():
        raise Exception(f"Can't find {mnemonic_path}")
    
    with open(mnemonic_path, "r") as file:
        return file.read().strip()

def generate_address(mnemonic):
    account = accounts.from_mnemonic(mnemonic, count=1)
    return account.address

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


oracle_pkh_1 = []
oracle_pkh_2 = []
master_pkh_1 = []
master_pkh_2 = []
master_pkh_3 = []

class LamportTest:
    
    def __init__(self):

        self.k1 = KeyTracker("Calmaster1") # new keys made here
        self.k2 = KeyTracker("Calmaster2")
        self.k3 = KeyTracker("Activityoracle1")
        self.k4 = KeyTracker("Activityoracle2")
        print("Initializing LamportTest...")
        with open('contract_LamportBase2-coin.txt', 'r') as file:
            contract_address = file.read().strip()
        #print(contract_address)
        self.contract = LamportBase2.at(contract_address)
        #lamport_base = LamportBase.at(contract_address) # <<< not working!
        accounts.default = str(accounts[0]) 
        # link it up
        pkhs = self.get_pkh_list(self.contract, 0)
        opkhs = self.get_pkh_list(self.contract, 1)
        # priv level set here with integer ^
        print("contract pkh", pkhs)

        self.load_two_masters(pkhs, "Calmaster")
        self.load_two_oracles(opkhs, "Activityoracle")
        print('init done')

    def get_pkh_list(self, contract, privilege_level):
        contract_pkh = str(contract.getPKHsByPrivilege(privilege_level))
        # gonna need some kind of wait / delay here for primetime
        print(contract_pkh)
        contract_pkh_list = re.findall(r'0x[a-fA-F0-9]+', contract_pkh)
        pkh_list = [pkh for pkh in contract_pkh_list]  # Removing '0x' prefix
        contract_pkh_string = json.dumps(contract_pkh)
        contract_pkh_list = json.dumps(contract_pkh_string)
        return pkh_list

    
    def load_two_masters(self, pkhs, filename):
        pkh_index = 0
        master1_loaded = False
        master2_loaded = False
        global master_pkh_1
        global master_pkh_2

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

        if not master2_loaded:
            print("Load failed for all provided PKHs for Master 2")

    def load_two_oracles(self, pkhs, filename):
        pkh_index = 0
        oracle1_loaded = False
        oracle2_loaded = False
        global oracle_pkh_1
        global oracle_pkh_2

        while not oracle1_loaded and pkh_index < len(pkhs):
            try:
                self.k3.load(self, filename + '1', pkhs[pkh_index])
                print(f"Load successful for Oracle 1, PKH: {pkhs[pkh_index]}")
                oracle1_loaded = True
                key_tracker_1 = self.k3.current_key_pair()
                oracle_pkh_1 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Oracle 1, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not oracle1_loaded:
            print("Load failed for all provided PKHs for Master 1")
            return

        while not oracle2_loaded and pkh_index < len(pkhs):
            try:
                self.k4.load(self, filename + '2', pkhs[pkh_index])
                print(f"Load successful for Oracle 2, PKH: {pkhs[pkh_index]}")
                oracle2_loaded = True
                key_tracker_2 = self.k4.current_key_pair()
                oracle_pkh_2 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Oracle 2, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not oracle2_loaded:
            print("Load failed for all provided PKHs for Master 2")

    # def load_keys(self, pkhs, filename):
    #     global oracle_pkh
    #     for pkh in pkhs:
    #         try:
    #             oracle_pkh = pkh
    #             self.k3.load(self, filename + '1', pkh)
    #             print(f"Load successful for PKH: {pkh}")
    #             return  # Exit function after successful load
    #         except InvalidAddress:
    #             print(f"No valid keys found for PKH: {pkh}")
    #             continue  # Try the next pkh if this one fails
    #     print("Load failed for all provided PKHs")

    def can_test_key_functions(self, accs):
        global master_pkh_1
        global master_pkh_2
        global oracle_pkh_1
        global oracle_pkh_2
        #global master_pkh_3
        print("Running 'can_test_key_functions'...")
        with open('contract_PlayerDatabase-coin.txt', 'r') as file:
            contract_address = file.read()
            contract_address = contract_address.strip().replace('\n', '')  # Remove whitespace and newlines

        _contract = PlayerDatabase.at(contract_address)
        print("Contract referenced.")
        print('oracle_pkh_1', oracle_pkh_1)
        private_key = '163f5f0f9a621d72fedd85ffca3d08d131ab4e812181e0d30ffd1c885d20aac7'
        brownie_account = accounts.add(private_key)
        current_keys = self.k3.load(self, "Activityoracle2", oracle_pkh_2)
        current_pkh = self.k3.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k3.get_next_key_pair()
        nextpkh = self.k3.pkh_from_public_key(next_keys.pub)
        #pairs = generate_address_value_pairs(10)
        #packed_pairs = solidity_pack_pairs(pairs)
        #_newCap = int(300000)
        #numToBroadcast = int(1000000)
        #pnumToBroadcast = numToBroadcast.to_bytes(4, 'big')
        #paddednumToBroadcast = solidity_pack_value_bytes(pnumToBroadcast)
        mnemonic1 = load_mnemonic('mnemonic1.txt')
        mnemonic2 = load_mnemonic('mnemonic2.txt')
        mnemonic3 = load_mnemonic('mnemonic3.txt')

        # Generate addresses
        #address = generate_address(mnemonic)
        address1 = generate_address(mnemonic1)
        address2 = generate_address(mnemonic2)
        address3 = generate_address(mnemonic3)
        serverPlayersLists = [
            {
                "serverIP": "172.93.101.194:27015",
                "playerNames": ["legopowa"]
            },
            {
                "serverIP": "63.143.56.124:27015",
                "playerNames": ["Player1", "Player2", "Player3"]
            },
            {
                "serverIP": "172.233.224.83:27015",
                "playerNames": ["PlayerE", "PlayerF"]
            }
        ]         
        formatted_lists = [
            (item["serverIP"], item["playerNames"]) for item in serverPlayersLists
        ]
        print(formatted_lists)

        data_to_hash = "192.168.1.1legopowa192.168.1.2PlayerBPlayerCPlayerD192.168.1.3PlayerEPlayerF".encode()

        #hashed_data = compute_keccak_hash(formatted_lists).encode()
        # Use web3.solidityKeccak to hash the data
        hashed_data = w3.solidity_keccak(['bytes'], [data_to_hash])
        #hashed_data = Web3.keccak(text=data_to_hash)
        print('hashed_data2', hashed_data.hex())
        # mnemonic_path = Path('mnemonic1.txt')
        # if not mnemonic_path.is_file():
        #     raise Exception(f"Can't find {mnemonic_path}")

        # with open(mnemonic_path, "r") as file:
        #     mnemonic = file.read().strip()
        mnemonic = load_mnemonic('mnemonic1.txt')
        # Generate the account using the mnemonic
        account = accounts.from_mnemonic(mnemonic)
        paddressToBroadcast = '0x742294571Ac5e19b28543beA69FD4955F9C7DA69' # Validator needing approval
        server_IP = '192.168.1.1'
        hashed_data = Web3.solidity_keccak(server_IP)
        #packed_message = str.lower(paddressToBroadcast)[2:].encode() + nextpkh[2:].encode() + ('1').encode()
        packed_message = hashed_data.hex()[2:].encode() + nextpkh[2:].encode()
        print(packed_message)
        print(str(packed_message.decode()))
        callhash = hash_b(str(packed_message.decode()))
        sig = sign_hash(callhash, current_keys.pri) 
        #private_key = '0x50e0105db0e25befff67c7596b91f72377b0fd8bb6f917ab46b91d7663fceb4c'
        #brownie_account = accounts.add(private_key)
        
        # _contract.updateGameServerIP(
        #     server_IP,
        #     2,
        #     current_keys.pub,
        #     sig,
        #     nextpkh,
        #     {'from': account, 'gas_limit': 3999999}    
        # )
        # self.k3.save(trim = False)
        # #self.k4.save(trim = False)
        # oracle_pkh_2 = nextpkh

        # #current_keys = self.k2.load(self, "Gmaster2", master_pkh_2)
        # #next_keys = self.k2.get_next_key_pair()
        # #nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        # #paddressToBroadcast = '0x742294571Ac5e19b28543beA69FD4955F9C7DA69'

        # packed_message = str.lower(paddressToBroadcast)[2:].encode() + nextpkh[2:].encode()

        # callhash = hash_b(str(packed_message.decode()))
        # sig = sign_hash(callhash, current_keys.pri) 


        # #validator = 0x72Bb7788cdA33503F247A818556c918f57cCa6c3
        gas_price = 2 * 10**9  # 2 gwei in wei
        gas_limit = 3000000  # Adjust as necessary

        _contract.submitPlayerListStepTwo(
            formatted_lists,
            address1,
            1,
            {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit}
        )


        #self.k2.save(trim = False)
        exit()