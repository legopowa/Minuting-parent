from brownie import SwapTest, accounts

def main():
    deployer_account = accounts.load('test2')
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 10000000  # Block gas limit in Ganache

    # Load addresses from files
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()
    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    # Deploy SwapTest contract
    swap_test = SwapTest.deploy(uniswap_router_address, custom_token_address, wmatic_address, {'from': deployer_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    
    # Write the address to a text file
    with open('./swap_test_address.txt', 'w') as f:
        f.write(swap_test.address)
    
    print(f"SwapTest contract deployed at: {swap_test.address}")

if __name__ == "__main__":
    main()
