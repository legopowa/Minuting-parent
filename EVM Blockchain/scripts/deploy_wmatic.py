from brownie import WrappedMatic, accounts

def main():
    # Load the account
    account = accounts.load('test2')

    # Deploy the WMATIC contract
    wmatic = WrappedMatic.deploy({'from': account})
    print(f"WMATIC deployed at: {wmatic.address}")

    # Save WMATIC address to a file
    with open('./wmatic_address.txt', 'w') as f:
        f.write(wmatic.address)
