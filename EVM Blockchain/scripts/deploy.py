from brownie import CalFundToken, accounts

def main():
    # Load the "test2" account
    deployer_account = accounts.load("test2")

    # Deploy the contract
    calfund_token = CalFundToken.deploy(
        deployer_account.address,
        {"from": deployer_account}
    )

    # Set up addresses
    uniswap_factory_address = "0x586A31a288E178369FFF020bA63d2224cf8661E9"
    uniswap_router_address = "0x13B4e811C99DAA2293e56f6987De4969AbD34dc3"
    wmatic_address = "0x6E6954F2412676e71a9B74850D1EEc61caa67fcA"
    #liquidity_pair_address = "0xDf28E94c11cb080b14d28F776700F1E05D6842E6"

    # Set contract addresses
    calfund_token.setUniswapFactory(uniswap_factory_address, {"from": deployer_account})
    calfund_token.setUniswapRouter(uniswap_router_address, {"from": deployer_account})
    calfund_token.setWmaticAddress(wmatic_address, {"from": deployer_account})
    #calfund_token.setUniswapPair(liquidity_pair_address, {"from": deployer_account})
    with open('./mintaddy.txt', 'w') as f:
        f.write(calfund_token.address)
    print(f"CalFundToken deployed at {calfund_token.address}")
