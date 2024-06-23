import os
from brownie import Activity_Mint, accounts

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

    # Read the initial authorized minter address from the file
    initial_authorized_minter = None
    try:
        with open('CalFund-commissionaddress.txt', 'r') as f:
            initial_authorized_minter = f.read().strip()
    except FileNotFoundError:
        print("Error: CalFund-commissionaddress.txt not found.")
        return

    # Request name and symbol via command line with default values
    name = input("Please input the token name (default 'Test'): ") or "Test"
    symbol = input("Please input the token symbol (default 'ATest'): ") or "ATest"

    # Deploy the contract
    your_contract = Activity_Mint.deploy(
        lamport_base_address,
        initial_authorized_minter,
        name,
        symbol,
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )

    # Output the contract address to a file
    with open('Activity-Mint.txt', 'w') as f:
        f.write(str(your_contract.address))

    print(f"Contract deployed at address: {your_contract.address}")
    print(f"Commission address used: {initial_authorized_minter}")
    print(f"LamportBase address used: {lamport_base_address}")
    print(f"Token name: {name}")
    print(f"Token symbol: {symbol}")
