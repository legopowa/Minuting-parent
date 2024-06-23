import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

from brownie import accounts, interface, network, CalFundToken, Contract
import os

def main():
    load_dotenv()

    # Connect to local Ganache node
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Inject Geth POA middleware

    # Check if the connection is successful
    if not web3.is_connected():
        print("Failed to connect to the Ethereum node.")
        return
    else:
        print("Connected to the Ethereum node.")
    
    # Load the "test2" account
    deployer_account = accounts.load("test2")
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Deploy the CalFundToken contract
    calfund_token = CalFundToken.deploy(
        deployer_account.address,
        {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )

    # Load addresses from the JSON file
    with open('deployedAddresses.json', 'r') as f:
        addresses = json.load(f)

    # Extract addresses
    uniswap_factory_address = addresses["factory"]
    uniswap_router_address = addresses["router"]
    wmatic_address = addresses["weth"]

    # Set contract addresses
    tx = calfund_token.setUniswapFactory(uniswap_factory_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)
    tx = calfund_token.setUniswapRouter(uniswap_router_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)
    tx = calfund_token.setWmaticAddress(wmatic_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)

    with open('./mintaddy.txt', 'w') as f:
        f.write(calfund_token.address)
    print(f"CalFundToken deployed at {calfund_token.address}")

    # Exchange 2 MATIC for 2 WMATIC
    wmatic = interface.IWETH(wmatic_address)
    tx = wmatic.deposit({'from': deployer_account, 'value': web3.to_wei(2, 'ether'), 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)
    print("2 MATIC exchanged for 2 WMATIC")

    # Instantiate the Uniswap V2 Router contract
    router = interface.IUniswapV2Router02(uniswap_router_address)

    # Approve the router to spend CalFundToken
    cal_amount = web3.to_wei(7500, 'ether')  # Adjust the amount as necessary
    wmatic_amount = web3.to_wei(2, 'ether')
    tx = calfund_token.approve(uniswap_router_address, cal_amount, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)
    print("Router approved to spend CAL tokens")

    # Approve the router to spend WMATIC
    tx = wmatic.approve(uniswap_router_address, wmatic_amount, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)
    print("Router approved to spend WMATIC")

    # Add liquidity to the CalFundToken-WMATIC pair
    tx = router.addLiquidity(
        calfund_token.address,
        wmatic_address,
        cal_amount,
        wmatic_amount,
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

    # Write the pair address to coinpair.txt
    with open('coinpair.txt', 'w') as f:
        f.write(pair_address)

    # Check if the pair exists
    if pair_address == '0x0000000000000000000000000000000000000000':
        raise ValueError("Pair does not exist. Ensure tokens are in the correct order and liquidity has been added.")

    # Set the Uniswap pair in the CalFundToken contract
    tx = calfund_token.setUniswapPair(pair_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)

    # ABI of the Uniswap V2 pair contract
    pair_abi = [
        {
            "inputs": [],
            "name": "getReserves",
            "outputs": [
                {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
                {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
                {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    # Load the pair contract
    pair_contract = Contract.from_abi("UniswapV2Pair", pair_address, pair_abi)

    # Call the getReserves function
    reserves = pair_contract.getReserves()
    reserve0, reserve1, block_timestamp_last = reserves

    # Print the reserves
    print(f"Reserves for pair {pair_address}:")
    print(f"Reserve 0: {reserve0}")
    print(f"Reserve 1: {reserve1}")
    print(f"Block Timestamp Last: {block_timestamp_last}")

if __name__ == "__main__":
    main()
