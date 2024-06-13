import os
from brownie import accounts, UniswapV2Factory, UniswapV2Router02, Contract, network
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

def main():
    # Load account
    dev = accounts.add(os.getenv("PRIVATE_KEY"))

    # Deploy Uniswap Factory
    factory = UniswapV2Factory.deploy(dev.address, {"from": dev})
    print(f"Factory deployed at: {factory.address}")

    # Deploy WETH contract (assuming WETH9)
    #WETH = Contract.from_explorer("0xce8699120ADDfF75325faB29AAdbA871F880D934")  # Mainnet WETH address

    # Deploy Uniswap Router
    router = UniswapV2Router02.deploy(factory.address, "0xce8699120ADDfF75325faB29AAdbA871F880D934", {"from": dev})
    print(f"Router deployed at: {router.address}")

    # Token addresses (replace with actual addresses)
    token_a = "0xd9623276393fb5F42981E7Ec241169Dc65674471"  # Example: DAI
    token_b = "0xce8699120ADDfF75325faB29AAdbA871F880D934"  # Example: WETH

    # Create pair
    tx = factory.createPair(token_a, token_b, {"from": dev})
    tx.wait(1)
    pair_address = factory.getPair(token_a, token_b)
    print(f"Pair created at: {pair_address}")

    return factory, router
