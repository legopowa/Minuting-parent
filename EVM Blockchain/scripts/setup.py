from brownie import CalFundToken, accounts

def main():
    # Load the test account
    test_account = accounts.load("test2")

    # Deploy the CalFundToken contract if not already deployed
    # Address of the deployed CalFundToken
    token_address = '0xA4a0F89C1835e2aA427322E2879E54e22F58b6E2'
    
    # Load the deployed CalFundToken contract
    token = CalFundToken.at(token_address)

    # Set the addresses for WMATIC, Uniswap Factory, and Router
    wmatic_address = "0x6E6954F2412676e71a9B74850D1EEc61caa67fcA"
    uniswap_factory_address = "0x586A31a288E178369FFF020bA63d2224cf8661E9"
    uniswap_router_address = "0x13B4e811C99DAA2293e56f6987De4969AbD34dc3"
    uniswap_pair_address = "0xD0Ea3bDBb274e3AAbBf359De0D49575Ddcc8ff4D"

    # Set the contract addresses in CalFundToken
    token.setWmaticAddress(wmatic_address, {'from': test_account})
    token.setUniswapFactory(uniswap_factory_address, {'from': test_account})
    token.setUniswapRouter(uniswap_router_address, {'from': test_account})
    token.setUniswapPair(uniswap_pair_address, {'from': test_account})
    token.setMaticAddress("0x0000000000000000000000000000000000001010", {'from': test_account})  # Native MATIC

    print("Contract addresses set successfully.")

if __name__ == "__main__":
    main()
