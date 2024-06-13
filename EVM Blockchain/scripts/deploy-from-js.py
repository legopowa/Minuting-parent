from brownie import CalFundToken, accounts
import json

def main():
    # Load the "test2" account
    deployer_account = accounts.load("test2")

    # Deploy the contract
    calfund_token = CalFundToken.deploy(
        deployer_account.address,
        {"from": deployer_account}
    )

    # Load addresses from the JSON file
    with open('deployedAddresses.json', 'r') as f:
        addresses = json.load(f)

    # Extract addresses
    uniswap_factory_address = addresses["factory"]
    uniswap_router_address = addresses["router"]
    wmatic_address = addresses["weth"]
    liquidity_pair_address = addresses["pair"]

    # Set contract addresses
    calfund_token.setUniswapFactory(uniswap_factory_address, {"from": deployer_account})
    calfund_token.setUniswapRouter(uniswap_router_address, {"from": deployer_account})
    calfund_token.setWmaticAddress(wmatic_address, {"from": deployer_account})
    calfund_token.setUniswapPair(liquidity_pair_address, {"from": deployer_account})

    with open('./mintaddy.txt', 'w') as f:
        f.write(calfund_token.address)
    print(f"CalFundToken deployed at {calfund_token.address}")
