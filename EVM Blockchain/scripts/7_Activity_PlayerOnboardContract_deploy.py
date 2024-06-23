import os
from brownie import PlayerOnboardContract, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Read the PlayerDatabase address from the file
    player_database_address = None
    try:
        with open('Activity-PlayerDatabase.txt', 'r') as f:
            player_database_address = f.read().strip()
    except FileNotFoundError:
        print("Error: Activity-PlayerDatabase.txt not found.")
        return

    # Deploy the contract
    player_onboard_contract = PlayerOnboardContract.deploy(
        player_database_address,
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )

    # Output the contract address to a file
    with open('Activity-PlayerOnboardContract.txt', 'w') as f:
        f.write(str(player_onboard_contract.address))

    print(f"Contract deployed at address: {player_onboard_contract.address}")
    print(f"PlayerDatabase address used: {player_database_address}")
