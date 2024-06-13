from brownie import accounts

def main():
    # Load the account
    account = accounts.load('test2')

    # Get the private key
    private_key = account.private_key

    # Print the private key
    print(f"Private key for account 'test2': {private_key}")
