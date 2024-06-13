import json
from web3 import Web3
from brownie import accounts, interface, network, CalFundToken
import os

def main():
    # Connect to Polygon Amoy Testnet node
    web3 = Web3(Web3.HTTPProvider('https://rpc-amoy.polygon.technology'))
    
    # Check if the connection is successful
    if not web3.is_connected():
        print("Failed to connect to the Ethereum node.")
        return
    else:
        print("Connected to the Ethereum node.")

    # Load the "test2" account
    deployer_account = accounts.load("test2")
    gas_price = 5 * 10**9  # 5 gwei in wei
    gas_limit = 10000000  # Adjust as necessary

    # Deploy the CalFundToken contract
    calfund_token = CalFundToken.deploy(
        deployer_account.address,
        {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    with open('./mintaddy.txt', 'w') as f:
        f.write(calfund_token.address)
    
    # Read Uniswap addresses from files
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()
    with open('./uniswap_factory_address.txt', 'r') as f:
        uniswap_factory_address = f.read().strip()

    # Set contract addresses
    calfund_token.setUniswapFactory(uniswap_factory_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    calfund_token.setUniswapRouter(uniswap_router_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    calfund_token.setWmaticAddress(wmatic_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Instantiate the Uniswap V2 Router contract
    router = interface.IUniswapV2Router02(uniswap_router_address)

    # Approve the router to spend CalFundToken
    token_amount = web3.toWei(10, 'ether')  # Adjust the amount as necessary
    calfund_token.approve(uniswap_router_address, token_amount, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Approve the router to spend WMATIC
    wmatic = interface.IERC20(wmatic_address)
    wmatic.approve(uniswap_router_address, token_amount, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Add liquidity to the CalFundToken-WMATIC pair
    tx = router.addLiquidity(
        calfund_token.address,
        wmatic_address,
        token_amount,
        token_amount,
        0,
        0,
        deployer_account.address,
        (web3.eth.get_block('latest').timestamp + 10000),  # Deadline in 10 minutes
        {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    tx.wait(1)  # Wait for the transaction to be mined

    print(f"Liquidity added: {tx}")

    # Instantiate the factory contract
    factory = interface.IUniswapV2Factory(uniswap_factory_address)

    # Get the pair address for the token and WMATIC
    pair_address = factory.getPair(calfund_token.address, wmatic_address)
    print(f"Pair address: {pair_address}")

if __name__ == "__main__":
    main()
