from brownie import CalFundToken, accounts, web3

def main():
    account = accounts.load('test2')

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    custom_token = CalFundToken.at(custom_token_address)

    # Set a reasonable gas price in wei (e.g., 50 gwei)
    gas_price = 2 * 10**9  # 2 gwei in wei (default gas price in Ganache)
    gas_limit = 30000000  # Block gas limit in Ganache
    # Ensure the total gas cost does not exceed the cap (1 Ether)
    # gas_cost = gas_limit * gas_price / 10**18  # Calculate total gas cost in Ether
    # if gas_cost > 1:  # Cap is 1 Ether
    #     gas_limit = int(1 * 10**18 / gas_price)

    try:
        # Assuming createPair function initializes the Uniswap pair and returns the pair address
        tx = custom_token.createPair({'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})

        # Retrieve the pair address from the transaction receipt
        pair_address = tx.events['PairCreated']['pair']

        # Write the pair address to coinpair.txt
        with open('./coinpair.txt', 'w') as f:
            f.write(pair_address)

        print(f"Uniswap Pair Address: {pair_address}")
    
    except Exception as e:
        # Print error details for debugging
        print(f"Transaction failed: {e}")
        print(f"Gas price: {gas_price}")
        print(f"Gas limit: {gas_limit}")
        print(f"Account balance: {web3.from_wei(account.balance(), 'ether')} Ether")
