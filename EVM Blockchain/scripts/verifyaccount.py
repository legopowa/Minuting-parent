from brownie import accounts

def main():
    # Load the newly created account without a password
    account = accounts.load('test2')
    print(f'The address of the new account is: {account.address}')
