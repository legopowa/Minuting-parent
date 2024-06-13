from brownie import convert, CalFundToken, WrappedMatic, UniswapV2Factory, UniswapV2Router02, accounts, network, web3

def main():
    deployer_account = accounts.load('test2')
    gas_price = 2 * 10**9  # 2 gwei in wei (default gas price in Ganache)
    gas_limit = 10000000  # Block gas limit in Ganache

    # Deploy UniswapV2Factory
    uniswap_factory = UniswapV2Factory.deploy(deployer_account.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    with open('./uniswap_factory_address.txt', 'w') as f:
        f.write(uniswap_factory.address)
    print(f"Uniswap Factory deployed at: {uniswap_factory.address}")

    # Deploy WrappedMatic
    wmatic = WrappedMatic.deploy({'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    with open('./wmatic_address.txt', 'w') as f:
        f.write(wmatic.address)
    print(f"Wrapped MATIC deployed at: {wmatic.address}")

    # Deposit MATIC to get WMATIC
    amount2 = convert.to_uint(1 * 10**18)  # Amount of MATIC to convert
    wmatic.deposit({'from': deployer_account, 'value': amount2, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Display WMATIC balance
    wmatic_balance = wmatic.balanceOf(deployer_account)
    print(f"WMATIC balance: {(wmatic_balance / 10**18), 'ether'} WMATIC")

    # Deploy UniswapV2Router01
    uniswap_router = UniswapV2Router02.deploy(uniswap_factory.address, wmatic.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    with open('./uniswap_router_address.txt', 'w') as f:
        f.write(uniswap_router.address)
    print(f"Uniswap Router deployed at: {uniswap_router.address}")

    # Deploy CalFundToken
    custom_token = CalFundToken.deploy({'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    with open('./mintaddy.txt', 'w') as f:
        f.write(custom_token.address)
    print(f"CalFundToken deployed at: {custom_token.address}")

    # Set contract addresses in CalFundToken
    custom_token.setUniswapFactory(uniswap_factory.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    custom_token.setUniswapRouter(uniswap_router.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    custom_token.setWmaticAddress(wmatic.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Create Pair
    custom_token.createPair({'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    pair_address = custom_token.getUniswapPair()
    print(f"Uniswap Pair Address: {pair_address}")
    custom_token.setUniswapPair(pair_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    with open('./coinpair.txt', 'w') as f:
        f.write(pair_address)
    print(f"Uniswap Pair Address: {pair_address}")

    # Adding Liquidity Example (commented out, but can be uncommented if needed)
    # amount_wmatic = 3 * 10**18  # 3 WMATIC
    # amount_token = 7500 * 10**18  # Equivalent amount of custom token

    # Approve tokens
    # wmatic.approve(uniswap_router.address, amount_wmatic, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    # custom_token.approve(uniswap_router.address, amount_token, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Add liquidity
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
