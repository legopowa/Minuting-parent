from brownie import LamportBase2, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary
    # Deploy the contract
    lamport_base2 = LamportBase2.deploy({'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Output the address to a file
    with open('Activity-LamportBase2.txt', 'w') as f:
        f.write(str(lamport_base2.address))

    print(f"Contract deployed at address: {lamport_base2.address}")
