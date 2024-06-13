from brownie import accounts
from eth_account import Account

def main():
    # Generate a new private key
    new_account = Account.create()
    private_key = new_account.key.hex()
    
    # Add the new account using the private key
    account = accounts.add(private_key)

    # Save the new account without a password
    account.save('user1', private_key, password='')

    # Print the new account address
    print(f'New account address: {account.address}')
