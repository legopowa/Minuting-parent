from brownie import accounts, interface

def main():
    # Load the account
    account = accounts.load('test2')

    # Read the token contract address from mintaddy.txt
    with open('./mintaddy.txt', 'r') as f:
        token_address = f.read().strip()

    # Load the token contract
    token = interface.IERC20(token_address)

    # Get the balance
    balance = token.balanceOf(account.address)

    # Assuming the token has 18 decimals
    balance_in_ether = balance / 10**18

    print(f"Token balance of test2: {balance_in_ether} TOKEN_SYMBOL")  # Replace TOKEN_SYMBOL with your token symbol

