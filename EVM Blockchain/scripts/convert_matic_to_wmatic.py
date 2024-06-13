from brownie import WrappedMatic, CalFundToken, accounts, convert

def main():
    account = accounts.load('test2')
    gas_price = 2 * 10**9  # 2 gwei in wei (default gas price in Ganache)
    gas_limit = 10000000  # Block gas limit in Ganache
    # Deploy WrappedMatic contract if not already deployed
    
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()
    wmatic = WrappedMatic.at(wmatic_address)
    #except FileNotFoundError:
    #    wmatic = WrappedMatic.deploy({'from': account})
       # with open('./wmatic_address.txt', 'w') as f:
    #        f.write(wmatic.address)

    # Convert MATIC to WMATIC
    amount = convert.to_uint(1 * 10**18)  # Amount of MATIC to convert
    wmatic.deposit({'from': account, 'value': amount, 'gas_price': gas_price, 'gas_limit': gas_limit})
    #print(f"Deposited {convert.from_uint(amount, 'ether')} MATIC to get WMATIC")

    # Display WMATIC balance
    wmatic_balance = wmatic.balanceOf(account)
    print(f"WMATIC balance: {(wmatic_balance / 10**18), 'ether'} WMATIC")
