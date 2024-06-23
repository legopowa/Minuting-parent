from brownie import accounts, interface

def main():
    # Load the account
    account = accounts.load('test2')

    # Read the token address from wmatic_address.txt
    with open('wmatic_address.txt', 'r') as file:
        token_address = file.read().strip()

    # Load the token contract
    token = interface.IERC20(token_address)

    # Get the balance
    balance = token.balanceOf(account.address)

    # Assuming the token has 18 decimals
    balance_in_ether = balance / 10**18

    print(f"wmatic balance of test2: {balance_in_ether} WMATIC")

if __name__ == "__main__":
    main()

