from brownie import accounts, UniswapV2Factory, WrappedMatic, UniswapV2Router01, network

def main():
    deployer_account = accounts.load("test2")
    gas_price = 50 * 10**9  # 50 gwei in wei
    gas_limit = 400000 * 10**9

    # Ensure the total gas cost does not exceed the cap (1 Ether)
    gas_cost = gas_limit * gas_price / 10**18  # Calculate total gas cost in Ether
    if gas_cost > 1:  # Cap is 1 Ether
        gas_limit = int(1 * 10**18 / gas_price)
    # Deploy UniswapV2Factory
    uniswap_factory = UniswapV2Factory.deploy(deployer_account.address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    factory_address = uniswap_factory.address
    print(f"UniswapV2Factory deployed at: {factory_address}")
    with open('./uniswap_factory_address.txt', 'w') as f:
        f.write(factory_address)

    # Deploy WrappedMatic
    wmatic = WrappedMatic.deploy({'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    wmatic_address = wmatic.address
    print(f"WrappedMatic deployed at: {wmatic_address}")
    with open('./wmatic_address.txt', 'w') as f:
        f.write(wmatic_address)

    # Deploy UniswapV2Router01
    uniswap_router = UniswapV2Router01.deploy(factory_address, wmatic_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    router_address = uniswap_router.address
    print(f"UniswapV2Router01 deployed at: {router_address}")
    with open('./uniswap_router_address.txt', 'w') as f:
        f.write(router_address)

    print("Deployment complete.")
