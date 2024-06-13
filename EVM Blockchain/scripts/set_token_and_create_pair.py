from brownie import CalFundToken, accounts

def main():
    account = accounts.load('test2')

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    custom_token = CalFundToken.at(custom_token_address)

    # Set the MATIC token address here (replace with actual MATIC address on Polygon)
    matic_address = "0x0000000000000000000000000000000000001010"
    custom_token.setMaticAddress(matic_address, {'from': account})

    # Assuming createPair function initializes the Uniswap pair and returns the pair address
    tx = custom_token.createPair({'from': account})
    
    # Retrieve the pair address from the transaction receipt
    pair_address = tx.events['PairCreated']['pair']

    # Write the pair address to coinpair.txt
    with open('./coinpair.txt', 'w') as f:
        f.write(pair_address)

    print("MATIC address set and pair created successfully.")
    print(f"Uniswap Pair Address: {pair_address}")
