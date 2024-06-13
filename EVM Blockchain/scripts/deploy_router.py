from brownie import UniswapV2Router01, accounts

def main():
    dev = accounts.load('test2')
    
    # Load WETH address from file
    with open('./wmatic_address.txt', 'r') as f:
        weth_address = f.read().strip()
    
    # Set the factory address
    factory_address = "0x586A31a288E178369FFF020bA63d2224cf8661E9"  # Replace with actual factory address
    
    # Deploy the UniswapV2Router01 contract
    router = UniswapV2Router01.deploy(factory_address, weth_address, {'from': dev})
    
    print(f"UniswapV2Router01 deployed at {router.address}")
    
    # Save the router address to a file
    with open('./uniswap_router_address.txt', 'w') as f:
        f.write(router.address)
