import os
from brownie import GameValidator, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Read the LamportBase address from the file
    lamport_base_address = None
    try:
        with open('Activity-LamportBase2.txt', 'r') as f:
            lamport_base_address = f.read().strip()
    except FileNotFoundError:
        print("Error: Activity-LamportBase2.txt not found.")
        return

    # Read the PlayerDatabase address from the file
    player_database_address = None
    try:
        with open('Activity-PlayerDatabase.txt', 'r') as f:
            player_database_address = f.read().strip()
    except FileNotFoundError:
        print("Error: Activity-PlayerDatabase.txt not found.")
        return

    # Read the MintContract address from the file
    mint_contract_address = None
    try:
        with open('Activity-Mint.txt', 'r') as f:
            mint_contract_address = f.read().strip()
    except FileNotFoundError:
        print("Error: Activity-Mint.txt not found.")
        return

    # Deploy the contract
    game_validator = GameValidator.deploy(
        lamport_base_address,
        player_database_address,
        mint_contract_address,
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )

    # Output the contract address to a file
    with open('Activity-GameValidator.txt', 'w') as f:
        f.write(str(game_validator.address))

    print(f"Contract deployed at address: {game_validator.address}")
    print(f"LamportBase address used: {lamport_base_address}")
    print(f"PlayerDatabase address used: {player_database_address}")
    print(f"MintContract address used: {mint_contract_address}")
