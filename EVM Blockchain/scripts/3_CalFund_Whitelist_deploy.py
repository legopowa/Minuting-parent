import os
from brownie import Whitelist, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts

    # Define gas price and gas limit
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Read the AnonID contract address from the file
    anonid_address = None
    try:
        with open('CalFund-AnonID.txt', 'r') as f:
            anonid_address = f.read().strip()
    except FileNotFoundError:
        print("Error: CalFund-AnonID.txt not found.")
        return

    # Deploy the Whitelist contract with the AnonID contract address as a constructor argument
    whitelist_contract = Whitelist.deploy(anonid_address, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Output the contract address to a file
    with open('CalFund-Whitelist.txt', 'w') as f:
        f.write(str(whitelist_contract.address))

    print(f"Whitelist contract deployed at address: {whitelist_contract.address}")
    print(f"AnonID contract address used: {anonid_address}")
