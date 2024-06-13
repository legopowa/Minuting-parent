from brownie import CalFundToken, accounts

def main():
    # Load the "test2" account
    deployer_account = accounts.load("test2")
    gas_price = 2 * 10**9  # 2 gwei in wei (default gas price in Ganache)
    gas_limit = 30000000  # Block gas limit in Ganache

    # Ensure the total gas cost does not exceed the cap (1 Ether)
    gas_cost = gas_limit * gas_price / 10**18  # Calculate total gas cost in Ether
    if gas_cost > 1:  # Cap is 1 Ether
        gas_limit = int(1 * 10**18 / gas_price)

    # Load contract address from mintaddy.txt
    with open('./mintaddy.txt', 'r') as f:
        calfund_token_address = f.read().strip()
    calfund_token = CalFundToken.at(calfund_token_address)

    # Load other addresses from files
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()
    with open('./uniswap_factory_address.txt', 'r') as f:
        uniswap_factory_address = f.read().strip()
    with open('./coinpair.txt', 'r') as f:
        liquidity_pair_address = f.read().strip()
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    # Set contract addresses
    calfund_token.setUniswapFactory(uniswap_factory_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    calfund_token.setUniswapRouter(uniswap_router_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    calfund_token.setWmaticAddress(wmatic_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    calfund_token.setUniswapPair(liquidity_pair_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    print(f"CalFundToken updated at {calfund_token.address}")
