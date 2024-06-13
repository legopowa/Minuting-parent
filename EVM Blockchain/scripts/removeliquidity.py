from brownie import accounts, interface, network, web3
from web3 import Web3

def main():
    # Connect to the network
    #network.connect('development')

    # Load the account
    account = accounts.load('test2')

    # Load addresses from files
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    with open('./coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    # Uniswap V2 Router and Factory addresses (replace with the correct addresses for your network)
    uniswap_router_address = '0x13B4e811C99DAA2293e56f6987De4969AbD34dc3'  # Example address

    # Instantiate the Uniswap V2 Router contract
    router = interface.IUniswapV2Router02(uniswap_router_address)

    # Instantiate the pair contract
    pair = interface.IUniswapV2Pair(pair_address)

    # Amount of liquidity tokens to remove
    liquidity = pair.balanceOf(account)

    # Approve the router to spend your liquidity tokens
    pair.approve(uniswap_router_address, liquidity, {'from': account})

    # Check allowances
    allowance = pair.allowance(account, uniswap_router_address)
    print(f"Allowance for router to spend liquidity tokens: {allowance}")

    # Ensure sufficient allowance
    if allowance < liquidity:
        raise ValueError("Insufficient allowance for liquidity tokens")

    # Call the removeLiquidity function
    tx = router.removeLiquidity(
        wmatic_address,
        '0xA4a0F89C1835e2aA427322E2879E54e22F58b6E2',
        liquidity,
        0,  # Minimum amount of WMATIC to receive
        0,  # Minimum amount of custom tokens to receive
        account.address,
        (web3.eth.get_block('latest')['timestamp'] + 1000),
        {'from': account}
    )

    print(f"Liquidity removed. Transaction hash: {tx.txid}")

if __name__ == "__main__":
    main()
