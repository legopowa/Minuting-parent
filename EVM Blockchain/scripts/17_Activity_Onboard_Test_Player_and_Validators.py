import os
from mnemonic import Mnemonic
from brownie import accounts, network, PlayerOnboardContract, PlayerDatabase

def get_address_from_mnemonic(mnemonic):
    # This function should derive the address from the mnemonic
    return accounts.from_mnemonic(mnemonic).address

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts

    # Define gas price and gas limit
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Read the PlayerOnboardContract address from file
    with open('Activity-PlayerOnboardContract.txt', 'r') as f:
        player_onboard_contract_address = f.read().strip()
    player_onboard_contract = PlayerOnboardContract.at(player_onboard_contract_address)

    # Initial player data
    user_data = [
        ("0x3Caddf9F0ea28EcCaaF3D971Db436f1f2Bf06351", "SteamID1", "legopowa", 1, 0, "0x3Caddf9F0ea28EcCaaF3D971Db436f1f2Bf06351")
    ]

    # Load mnemonics and prepare player data
    for i in range(1, 4):
        with open(f'mnemonic{i}.txt', 'r') as f:
            mnemonic = f.read().strip()
        address = get_address_from_mnemonic(mnemonic)
        steam_id = f"SteamID{i+1}"
        player_name = f"Player{i}"
        oracle_key_index1 = i + 1
        oracle_key_index2 = 0
        reward_address = address
        user_data.append((address, steam_id, player_name, oracle_key_index1, oracle_key_index2, reward_address))
        print(address, player_name, oracle_key_index1)
    # Onboard each player
    for data in user_data:
        _address, _steamID, _playerName, _oracleKeyIndex1, _oracleKeyIndex2, _rewardAddress = data
        tx = player_onboard_contract.onboardPlayer(
            _address,
            _steamID,
            _playerName,
            _oracleKeyIndex1,
            _oracleKeyIndex2,
            _rewardAddress,
            {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
        )
        tx2 = player_onboard_contract.registerValidator(
            _address
        )
        print(f"Onboarded {_address} as a validator, with SteamID {_steamID} and player name {_playerName}")

    print("Player onboarding complete.")