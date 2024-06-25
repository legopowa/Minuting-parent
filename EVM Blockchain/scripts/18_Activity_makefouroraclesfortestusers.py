import lorem

import sys
from itertools import chain
import random
import hashlib
import base64
from web3 import Web3
from web3.exceptions import InvalidAddress
from brownie import web3, accounts, Wei, LamportBase2, Contract
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



gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

# if network.show_active() == "development":
gas_price(gas_strategy)

# ITERATIONS = 3

# def compute_crc(self, data: str) -> int:
#     return crc32(data.encode())

offchain.data_temp.received_data = b''

def encode_packed(*args):
    return b"".join([struct.pack(f"<{len(arg)}s", arg) for arg in args])

# def solidity_pack_pairs(pairs):
#     packed_pairs = []
#     for pair in pairs:
#         address = pair[0]
#         value = pair[1]
#         packed_pairs.append(solidity_pack_bytes([address, value]))
#     return b''.join(packed_pairs)

# def solidity_pack_bytes(values):
#     packed_values = []

#     for value in values:
#         if isinstance(value, int):
#             # solidity uses big endian
#             packed_value = value.to_bytes((value.bit_length() + 7) // 8, 'big').rjust(32, b'\0')
#         elif isinstance(value, str) and re.match(r"^0x[a-fA-F0-9]{40}$", value):
#             packed_value = bytes.fromhex(value[2:]).rjust(32, b'\0')
#         elif isinstance(value, str):
#             packed_value = value.encode('utf-8')
#         else:
#             raise ValueError("Unsupported type")
            
#         packed_values.append(packed_value)

    return b''.join(packed_values)
def generate_address_value_pairs(n_pairs):
    pairs = [[None, None]] * 10
    for i in range(n_pairs):
        address = '0x' + binascii.hexlify(os.urandom(20)).decode()  # An Ethereum address is 20 bytes
        value = random.randint(1, 1000)  # You can adjust this as per your needs
        pairs[i][0] = address
        pairs[i][1] = value
    return pairs
# def generate_address_value_pairs(n):

#         addr = generate_address()  # Replace with your own logic to generate an address
#         value = generate_value()  # Replace with your own logic to generate a value
 
def custom_encode_packed(address, integer):
    # Convert the address to bytes and pad with zeroes
    address_bytes = bytes(Web3.toBytes(hexstr=address))

    # Convert the integer to bytes and pad with zeroes
    integer_bytes = encode('uint', integer)

    # Concatenate everything together
    result = address_bytes + b'\0' * 12 + integer_bytes + b'\0' * 12

    return result.decode('unicode_escape')

def main():
    
    
    lamport_test = LamportTest()
        
        # Convert all account objects to strings before passing them
    lamport_test.can_test_key_functions([str(acc) for acc in accounts])
    #lamport_test.can_test_message_functions([str(acc) for acc in accounts])
    #lamport_test.can_test_del_functions([str(acc) for acc in accounts])       

        # lamport_test.load_keys()
        # lamport_test.load_two_masters()

        # lamport_test.can_broadcast_message_via_broadcast2([str(acc) for acc in accounts])
        # lamport_test.can_broadcast_message_via_broadcast_with_number([str(acc) for acc in accounts])
        # lamport_test.can_broadcast_message_via_broadcast_with_number_and_address([str(acc) for acc in accounts])
        
#port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

oracle_pkh_1 = []
oracle_pkh_2 = []
oracle_pkh_3 = []
oracle_pkh_4 = []
master_pkh_1 = []
master_pkh_2 = []
master_pkh_3 = []
master_pkh_4 = []


class LamportTest:
    
    def __init__(self):

        self.k1 = KeyTracker("Activitymaster1") # new keys made here
        self.k2 = KeyTracker("Activitymaster2")
        self.k3 = KeyTracker("Activityoracle1")
        self.k4 = KeyTracker("Activityoracle2")
        self.k5 = KeyTracker("Activityoracle3")
        self.k6 = KeyTracker("Activityoracle4")
        
        print("Initializing LamportBase2...")
        with open('Activity-LamportBase2.txt', 'r') as file:
            contract_address = file.read()
        self.contract = LamportBase2.at(contract_address)
        #lamport_base = LamportBase.at(contract_address) # <<< not working!
        deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts
        accounts.default = deployer  # Set test2 as the default account
        # link it up
        pkhs = self.get_pkh_list(self.contract, 0)
        opkhs = self.get_pkh_list(self.contract, 1)
        # priv level set here with integer ^
        print("contract pkh", pkhs)

        self.load_two_masters(pkhs, "Activitymaster")
        self.load_four_oracles(opkhs, "Activityoracle")
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

    def load_four_oracles(self, pkhs, filename):
        pkh_index = 0
        oracle1_loaded = False
        oracle2_loaded = False
        oracle3_loaded = False
        oracle4_loaded = False
        global oracle_pkh_1
        global oracle_pkh_2
        global oracle_pkh_3
        global oracle_pkh_4

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
            print("Load failed for all provided PKHs for Oracle 1")
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
            print("Load failed for all provided PKHs for Oracle 2")

        while not oracle3_loaded and pkh_index < len(pkhs):
            try:
                self.k5.load(self, filename + '3', pkhs[pkh_index])
                print(f"Load successful for Oracle 3, PKH: {pkhs[pkh_index]}")
                oracle3_loaded = True
                key_tracker_3 = self.k5.current_key_pair()
                oracle_pkh_3 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Oracle 3, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not oracle3_loaded:
            print("Load failed for all provided PKHs for Oracle 3")

        while not oracle4_loaded and pkh_index < len(pkhs):
            try:
                self.k6.load(self, filename + '4', pkhs[pkh_index])
                print(f"Load successful for Oracle 4, PKH: {pkhs[pkh_index]}")
                oracle4_loaded = True
                key_tracker_4 = self.k6.current_key_pair()
                oracle_pkh_4 = pkhs[pkh_index]
                pkh_index += 1  # increment the pkh_index after successful load
            except InvalidAddress:
                print(f"No valid keys found for Oracle 4, PKH: {pkhs[pkh_index]}")
                pkh_index += 1  # increment the pkh_index if load failed

        if not oracle4_loaded:
            print("Load failed for all provided PKHs for Oracle 4")  


#    def load_keys(self, pkhs, filename):
#        global oracle_pkh
#        for pkh in pkhs:
#            try:
#                oracle_pkh = pkh
#                self.k3.load(self, filename + '1', pkh)
#                print(f"Load successful for PKH: {pkh}")
#                return  # Exit function after successful load
#            except InvalidAddress:
#                print(f"No valid keys found for PKH: {pkh}")
#                continue  # Try the next pkh if this one fails
#        print("Load failed for all provided PKHs")

    def can_test_key_functions(self, accs):
        
        global master_pkh_1
        global master_pkh_2
        global oracle_pkh_1
        global oracle_pkh_2
        global oracle_pkh_3
        global oracle_pkh_4
        print("Running 'can_test_key_functions'...")
        with open('Activity-LamportBase2.txt', 'r') as file:
            contract_address = file.read()
        _contract = LamportBase2.at(contract_address)
        print("Contract referenced.")
        print('master_pkh_1', master_pkh_1)


        # pairs = generate_address_value_pairs(10)
        # packed_pairs = solidity_pack_pairs(pairs)


        # packed_message = binascii.hexlify(packed_pairs) + nextpkh[2:].encode()
        # callhash = hash_b(str(packed_message.decode()))
        # sig = sign_hash(callhash, current_keys.pri) 
        # _contract.contractCallTest(
                            
        #     pairs,
        #     current_keys.pub,
        #     nextpkh,
        #     sig,
        #     {'from': str(accs[0])}

        # )
        #self.k1.save(trim = False)
        #master_pkh_1 = nextpkh
    

        # verification_failed_filter = _contract.events.VerificationFailed.createFilter(fromBlock='latest')

        # for event in verification_failed_filter.get_all_entries():
        #     hashed_data = event['args']['hashedData']
        #     print(f"Verification failed for hashed data: {hashed_data}")
        
        # address_value_pairs_filter = _contract.events.AddressValuePairsBroadcasted.createFilter(fromBlock='latest')
        # for event in address_value_pairs_filter.get_all_entries():
        #     pairs = event['args']['pairs']
        #     print(f"Address-Value pairs: {pairs}")

        current_keys = self.k1.load(self, "Activitymaster1", master_pkh_1)
        current_pkh = self.k1.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k1.get_next_key_pair()
        nextpkh = self.k1.pkh_from_public_key(next_keys.pub)

        oracletestkeys = self.k3.get_next_key_pair()
        mtk_pkh = self.k3.pkh_from_public_key(oracletestkeys.pub)
        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k1.save(trim = False)
        self.k3.save(trim = False)
        master_pkh_1 = nextpkh

        current_keys = self.k2.load(self, "Activitymaster2", master_pkh_2)
        next_keys = self.k2.get_next_key_pair()
        nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepTwo(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k2.save(trim = False)
        self.k3.save(trim = False)
       
        master_pkh_2 = nextpkh
        oracle_pkh_1 = mtk_pkh

        current_keys = self.k1.load(self, "Activitymaster1", master_pkh_1)
        current_pkh = self.k1.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k1.get_next_key_pair()
        nextpkh = self.k1.pkh_from_public_key(next_keys.pub)

        oracletestkeys = self.k4.get_next_key_pair()
        mtk_pkh = self.k4.pkh_from_public_key(oracletestkeys.pub)
        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k1.save(trim = False)
        self.k4.save(trim = False)
        master_pkh_1 = nextpkh

        current_keys = self.k2.load(self, "Activitymaster2", master_pkh_2)
        next_keys = self.k2.get_next_key_pair()
        nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepTwo(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k2.save(trim = False)
        self.k4.save(trim = False)
       
        master_pkh_2 = nextpkh
        oracle_pkh_2 = mtk_pkh
        
        current_keys = self.k1.load(self, "Activitymaster1", master_pkh_1)
        current_pkh = self.k1.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k1.get_next_key_pair()
        nextpkh = self.k1.pkh_from_public_key(next_keys.pub)

        oracletestkeys = self.k5.get_next_key_pair()
        mtk_pkh = self.k5.pkh_from_public_key(oracletestkeys.pub)
        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k1.save(trim = False)
        self.k5.save(trim = False)
        master_pkh_1 = nextpkh

        current_keys = self.k2.load(self, "Activitymaster2", master_pkh_2)
        next_keys = self.k2.get_next_key_pair()
        nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepTwo(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k2.save(trim = False)
        self.k5.save(trim = False)
       
        master_pkh_2 = nextpkh
        oracle_pkh_2 = mtk_pkh

        current_keys = self.k1.load(self, "Activitymaster1", master_pkh_1)
        current_pkh = self.k1.pkh_from_public_key(current_keys.pub)
        print('current pkh', current_pkh)
        next_keys = self.k1.get_next_key_pair()
        nextpkh = self.k1.pkh_from_public_key(next_keys.pub)

        oracletestkeys = self.k6.get_next_key_pair()
        mtk_pkh = self.k6.pkh_from_public_key(oracletestkeys.pub)
        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepOne(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k1.save(trim = False)
        self.k6.save(trim = False)
        master_pkh_1 = nextpkh

        current_keys = self.k2.load(self, "Activitymaster2", master_pkh_2)
        next_keys = self.k2.get_next_key_pair()
        nextpkh = self.k2.pkh_from_public_key(next_keys.pub)

        packed_message = mtk_pkh[2:] + nextpkh[2:]
        callhash = hash_b(packed_message)
        sig = sign_hash(callhash, current_keys.pri) 

        
        _contract.createOracleKeyStepTwo(
            current_keys.pub,
            sig,
            nextpkh,
            mtk_pkh[2:],
            {'from': str(accs[0])}    
        )
        self.k2.save(trim = False)
        self.k6.save(trim = False)
       
        master_pkh_2 = nextpkh
        oracle_pkh_3 = mtk_pkh
        opkhs = self.get_pkh_list(_contract, 1)
        self.load_four_oracles(opkhs, "Activityoracle")

        ## If you load the same key twice it'll revert

    # def can_test_message_functions(self, accs):
    #     global master_pkh_1
    #     global master_pkh_2
    #     global master_pkh_3
    #     global oracle_pkh
    #     print("Running 'can_test_message_functions'...")
    #     with open('contract.txt', 'r') as file:
    #         contract_address = file.read()
    #     _contract = LamportTest2.at(contract_address)
    #     print("Contract referenced.")
        
    #     current_keys = self.k4.load(self, "master3", master_pkh_3)
    #     current_pkh = self.k4.pkh_from_public_key(current_keys.pub)
    #     print('current pkh', current_pkh)
    #     next_keys = self.k4.get_next_key_pair()
    #     nextpkh = self.k4.pkh_from_public_key(next_keys.pub)
    #     pairs = generate_address_value_pairs(10)
    #     packed_pairs = solidity_pack_pairs(pairs)

    #     testmessage = lorem.sentence()
    #     ptestmessage = solidity_pack_bytes(testmessage)

    #     numToBroadcast = random.randint(0, 1000000)
    #     pnumToBroadcast = numToBroadcast.to_bytes(4, 'big')
    #     paddednumToBroadcast = solidity_pack_value_bytes(pnumToBroadcast)

    #     paddressToBroadcast = accs[0]

    #     sleep(4)

    #     packed_message = packed_pairs.hex() + ptestmessage.hex() + paddednumToBroadcast.hex() + str.lower(paddressToBroadcast[2:]) + nextpkh[2:]
    #     callhash = hash_b(packed_message)
    #     sig = sign_hash(callhash, current_keys.pri) 
        
    #     nextpkh_bytes = bytes.fromhex(nextpkh[2:])

    #     # print("packed pairs", packed_pairs.hex())
    #     # print("ptestmessage", ptestmessage.hex())
    #     # print("pnumToBroadcast", paddednumToBroadcast.hex())
    #     # print("paddressToBroadcast", str.lower(paddressToBroadcast[2:]))
    #     # print("nextpkh", nextpkh[2:])
    #     # print("packed_message =", packed_message)

    #     _contract.contractCallTest2(
            
    #         pairs,
    #         current_keys.pub,
    #         testmessage,
    #         numToBroadcast,
    #         paddressToBroadcast,
    #         sig,
    #         nextpkh,
    #         {'from': str(accs[0])}
            
    #         )
        
    #     self.k4.save(trim = False)
    #     master_pkh_3 = nextpkh
    #     # Create a filter for the VerificationFailed event
    #     verification_failed_filter = _contract.events.VerificationFailed.createFilter(fromBlock='latest')

    #     # Loop through all entries from the VerificationFailed event
    #     for event in verification_failed_filter.get_all_entries():
    #         hashed_data = event['args']['hashedData']
    #         print(f"Verification failed for hashed data: {hashed_data}")
        
    #     event_filter = _contract.events.EncodedPairs.createFilter(fromBlock='latest')

    #     # Then, to get the new event entries:
    #     sleep(2)
    #     new_entries = event_filter.get_all_entries()

    #     for event in new_entries:
    #         encoded_pairs = event['args']['encodedPairs']
    #     print("encoded pairs", encoded_pairs.hex())
        
    # def can_test_del_functions(self, accs):
    #     global master_pkh_1
    #     global master_pkh_2
    #     global master_pkh_3
    #     print("Running 'can_test_key_functions'...")
    #     with open('contract.txt', 'r') as file:
    #         contract_address = file.read()
    #     _contract = LamportTest2.at(contract_address)
    #     print("Contract referenced.")
    #     print('master_pkh_1', master_pkh_1)

    #     current_keys = self.k1.load(self, "master1", master_pkh_1)
    #     current_pkh = self.k1.pkh_from_public_key(current_keys.pub)
    #     print('current pkh', current_pkh)
    #     next_keys = self.k1.get_next_key_pair()
    #     nextpkh = self.k1.pkh_from_public_key(next_keys.pub)

    #     mtk_pkh = master_pkh_3
    #     packed_message = mtk_pkh[2:] + nextpkh[2:]
    #     callhash = hash_b(packed_message)
    #     sig = sign_hash(callhash, current_keys.pri) 

    #     _contract.deleteKeyStepOne(
    #         current_keys.pub,
    #         sig,
    #         nextpkh,
    #         mtk_pkh[2:],
    #         {'from': str(accs[0])}    
    #     )
    #     self.k1.save(trim = False)

    #     current_keys = self.k2.load(self, "master2", master_pkh_2)
    #     current_pkh = self.k2.pkh_from_public_key(current_keys.pub)
    #     print('current pkh', current_pkh)
    #     next_keys = self.k2.get_next_key_pair()
    #     nextpkh = self.k2.pkh_from_public_key(next_keys.pub)


    #     packed_message = mtk_pkh[2:] + nextpkh[2:]
        
    #     callhash = hash_b(packed_message)
    #     sig = sign_hash(callhash, current_keys.pri) 
        
    #     _contract.deleteKeyStepTwo(
    #         current_keys.pub,
    #         sig,
    #         nextpkh,
    #         mtk_pkh[2:],
    #         {'from': str(accs[0])}    
    #     )
    #     self.k2.save(trim = False)

    #     ## If you load the same key twice it'll revert; this prevents you from 
    #     ## deleting the master keys used for the process as well (due to how you need
    #     ## new public key hashes per transaction with lamport keys, and getting the same 
    #     ## one twice is basically impossible, and you also need a non-changing public key
    #     ## hash to persist between the two steps; this is a good chanced-upon 
    #     ## self-preservation mechanism)
        
# if __name__ == "__main__":
#     main()