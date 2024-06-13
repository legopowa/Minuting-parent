from brownie import CalFundToken, accounts

def main():
    account = accounts.load('test2')

    # Load the pair address from coinpair.txt
    with open('./coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    # Load the custom token contract address from mintaddy.txt
    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    # Instantiate the custom token contract
    custom_token = CalFundToken.at(custom_token_address)

    # Set the Uniswap pair address
    tx = custom_token.setUniswapPair(pair_address, {'from': account})

    print(f"Uniswap pair set. Transaction hash: {tx.txid}")
