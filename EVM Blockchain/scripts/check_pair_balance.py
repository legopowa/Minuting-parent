from brownie import accounts, interface, Contract, network
 
from web3 import Web3

def main():
    # Connect to the network
    #network.connect('development')

    # Load account
    account = accounts.load('test2')

    # Load addresses from files
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()
        
    with open('./uniswap_factory_address.txt', 'r') as f:
        uniswap_factory_address = f.read().strip()

    # Address of the Uniswap V2 Factory
    # = '0x586A31a288E178369FFF020bA63d2224cf8661E9'  # Uniswap V2 factory address

    # Instantiate the factory contract
    factory = interface.IUniswapV2Factory(uniswap_factory_address)

    # Get the pair address for the token and WMATIC
    #pair_address = factory.getPair(wmatic_address, custom_token_address)
    pair_address = factory.getPair(custom_token_address, wmatic_address)
    print(f"Pair address: {pair_address}")

    # Check if the pair exists
    if pair_address == '0x0000000000000000000000000000000000000000':
        raise ValueError("Pair does not exist. Ensure tokens are in the correct order and liquidity has been added.")

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
