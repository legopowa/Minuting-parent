from brownie import WrappedMatic, accounts, convert

def main():
    account = accounts.load('test2')

    # Load WrappedMatic contract
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()
    wmatic = WrappedMatic.at(wmatic_address)

    # Amount of WMATIC to withdraw (convert to MATIC)
    amount = convert.to_uint(3 * 10**18)  # 3 WMATIC

    # Withdraw WMATIC to get MATIC
    wmatic.withdraw(amount, {'from': account})

    # Display WMATIC balance after withdrawal
    wmatic_balance = wmatic.balanceOf(account)
    print(f"WMATIC balance: {wmatic_balance / 10**18} WMATIC")

    # Display MATIC balance after withdrawal
    matic_balance = account.balance()
    print(f"MATIC balance: {matic_balance / 10**18} MATIC")
