from brownie import WrappedMatic, accounts, convert

def main():
    account = accounts.load('test2')
    gas_price = 2 * 10**9  # 2 gwei in wei (default gas price in Ganache)
    gas_limit = 10000000  # Block gas limit in Ganache

    # Load or deploy the WrappedMatic contract

    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()
    wmatic = WrappedMatic.at(wmatic_address)
#    except FileNotFoundError:
#        wmatic = WrappedMatic.deploy({'from': account})
#        with open('./wmatic_address.txt', 'w') as f:
#            f.write(wmatic.address)

    # Withdraw all WMATIC to get MATIC
    wmatic_balance = wmatic.balanceOf(account)
    if wmatic_balance > 0:
        wmatic.withdraw(wmatic_balance, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})
        print(f"Withdrew {convert.from_uint(wmatic_balance, 'ether')} WMATIC to get MATIC")

    # Display the final MATIC balance
    matic_balance = account.balance()
    print(f"MATIC balance: {convert.from_uint(matic_balance, 'ether')} MATIC")

if __name__ == "__main__":
    main()
