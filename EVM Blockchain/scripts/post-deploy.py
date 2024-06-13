from brownie import convert, CalFundToken, WrappedMatic, UniswapV2Factory, UniswapV2Router01, accounts, interface, web3

def main():
    deployer_account = accounts.load('test2')
    gas_price = 2 * 10**9  # 2 gwei in wei (default gas price in Ganache)
    gas_limit = 10000000  # Block gas limit in Ganache

    # Read UniswapV2Factory address from file
    with open('./uniswap_factory_address.txt', 'r') as f:
        uniswap_factory_address = f.read().strip()
    uniswap_factory = UniswapV2Factory.at(uniswap_factory_address)
    print(f"Uniswap Factory deployed at: {uniswap_factory.address}")

    # Read WrappedMatic address from file
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()
    wmatic = WrappedMatic.at(wmatic_address)
    print(f"Wrapped MATIC deployed at: {wmatic.address}")

    amount2 = convert.to_uint(1 * 10**18)  # Amount of MATIC to convert
    wmatic.deposit({'from': deployer_account, 'value': amount2, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Display WMATIC balance
    wmatic_balance = wmatic.balanceOf(deployer_account)
    print(f"WMATIC balance: {(wmatic_balance / 10**18), 'ether'} WMATIC")

    # Read UniswapV2Router02 address from file
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()
    uniswap_router = UniswapV2Router01.at(uniswap_router_address)
    print(f"Uniswap Router deployed at: {uniswap_router.address}")

    # Load CalFundToken address from file
    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()
    custom_token = CalFundToken.at(custom_token_address)

    # Set contract addresses
    custom_token.setUniswapFactory(uniswap_factory.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    custom_token.setUniswapRouter(uniswap_router.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    custom_token.setWmaticAddress(wmatic.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Create Pair
    custom_token.createPair({'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    pair_address = custom_token.getUniswapPair()
    print(pair_address)
    custom_token.setUniswapPair(pair_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    with open('./coinpair.txt', 'w') as f:
        f.write(pair_address)
    print(f"Uniswap Pair Address: {pair_address}")

    # # Adding Liquidity Example
    # amount_wmatic = 3 * 10**18  # 3 WMATIC
    # amount_token = 7500 * 10**18  # Equivalent amount of custom token

    # # Approve tokens
    # wmatic.approve(uniswap_router.address, amount_wmatic, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    # custom_token.approve(uniswap_router.address, amount_token, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # # Add liquidity
    # tx = custom_token.addLiquidity(
    #     amount_wmatic,
    #     amount_token,
    #     0,  # Min WMATIC amount
    #     0,  # Min token amount
    #     web3.eth.get_block('latest')['timestamp'] + 1000,
    #     {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit}
    # )
    # print(f"Liquidity added. Transaction hash: {tx.txid}")

if __name__ == "__main__":
    main()
