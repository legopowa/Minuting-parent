import os
from brownie import PlayerDatabase, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts
    gas_price = 5 * 10**9  # 2 gwei in wei
    gas_limit = 10000000  # Adjust as necessary

    # Read the LamportBase address from the file
    lamport_base_address = None
    try:
        with open('Activity-LamportBase2.txt', 'r') as f:
            lamport_base_address = f.read().strip()
    except FileNotFoundError:
        print("Error: Activity-LamportBase2.txt not found.")
        return

    # Read the AnonID address from the file
    anon_id_address = None
    try:
        with open('CalFund-AnonID.txt', 'r') as f:
            anon_id_address = f.read().strip()
    except FileNotFoundError:
        print("Error: CalFund-AnonID.txt not found.")
        return

    # Deploy the contract
    player_database = PlayerDatabase.deploy(
        lamport_base_address,
        anon_id_address,
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )

    # Output the contract address to a file
    with open('Activity-PlayerDatabase.txt', 'w') as f:
        f.write(str(player_database.address))

    print(f"Contract deployed at address: {player_database.address}")
    print(f"LamportBase address used: {lamport_base_address}")
    print(f"AnonID address used: {anon_id_address}")
