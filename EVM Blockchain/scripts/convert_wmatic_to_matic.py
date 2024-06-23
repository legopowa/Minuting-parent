from brownie import accounts, interface, network, web3
import json
import os
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables
    load_dotenv()

    # Set up the deployer account
    deployer = accounts.load('test2')
    print('Interacting with contracts using the account:', deployer.address)

    # Load the WMATIC address from wmatic_address.txt
    with open('wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    # Set up the WMATIC contract object
    wmatic = interface.IWETH(wmatic_address)

    # Display deployer's WMATIC balance
    wmatic_balance = wmatic.balanceOf(deployer.address)
    print('Deployer WMATIC balance:', web3.from_wei(wmatic_balance, 'ether'))

    # Convert all WMATIC to MATIC
    if wmatic_balance > 0:
        wmatic.withdraw(wmatic_balance, {'from': deployer}).wait(1)
        print('Converted all WMATIC to MATIC')

    # Display deployer's new MATIC balance
    new_matic_balance = web3.eth.get_balance(deployer.address)
    print('Deployer new MATIC balance:', web3.from_wei(new_matic_balance, 'ether'))

if __name__ == "__main__":
    main()
