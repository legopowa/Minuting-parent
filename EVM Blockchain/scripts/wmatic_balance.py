from brownie import accounts, interface

def main():
    # Load the account
    account = accounts.load('test2')

    # Token contract address
    token_address = "0x6E6954F2412676e71a9B74850D1EEc61caa67fcA"

    # Load the token contract
    token = interface.IERC20(token_address)

    # Get the balance
    balance = token.balanceOf(account.address)

    # Assuming the token has 18 decimals
    balance_in_ether = balance / 10**18

    print(f"wmatic balance of polygon_dev: {balance_in_ether} TOKEN_SYMBOL")  # Replace TOKEN_SYMBOL with your token symbol
