from brownie import UniswapV2Pair, network, web3

def main():
    # Ensure you are on the correct network (use 'development' or 'ganache-local' for local testing)
    #network.connect('development')

    # Get the bytecode of the compiled UniswapV2Pair contract
    bytecode = UniswapV2Pair.bytecode

    # Calculate the init code hash
    init_code_hash = web3.keccak(bytecode).hex()
    print(f"Init code hash: {init_code_hash}")

    # Optionally save the init code hash to a file
    with open('./init_code_hash.txt', 'w') as f:
        f.write(init_code_hash)

if __name__ == "__main__":
    main()
