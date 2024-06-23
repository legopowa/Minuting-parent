import os
from brownie import AnonIDContract, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Request the coin commission address via command line
    commission_address = input("Please input coin commission address: ")
    coin_commission = int(input("Please input the coin commission (as a percentage): "))

    # Read the LamportBase address from the file
    lamport_base_address = None
    try:
        with open('CalFund-LamportBase2.txt', 'r') as f:
            lamport_base_address = f.read().strip()
    except FileNotFoundError:
        print("Error: CalFund-LamportBase2.txt not found.")
        return

    # Deploy the contract
    anon_id_contract = AnonIDContract.deploy(
        commission_address, 
        lamport_base_address,
        coin_commission,
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )

    # Output the contract address to a file
    with open('CalFund-AnonID.txt', 'w') as f:
        f.write(str(anon_id_contract.address))

    # Output the commission address to a file
    with open('CalFund-commissionaddress.txt', 'w') as f:
        f.write(commission_address)

    print(f"Contract deployed at address: {anon_id_contract.address}")
    print(f"Commission address saved to CalFund-commissionaddress.txt")
