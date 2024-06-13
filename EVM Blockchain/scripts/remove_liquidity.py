from brownie import interface, accounts, convert, web3

def main():
    account = accounts.load('test2')

    # Load addresses from files
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    with open('./coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    # Uniswap V2 Router address
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()
        
    # Instantiate contracts
    uniswap_router = interface.IUniswapV2Router02(uniswap_router_address)
    pair = interface.IUniswapV2Pair(pair_address)
    wmatic = interface.IERC20(wmatic_address)
    custom_token = interface.IERC20(custom_token_address)

    # Amount of LP tokens to remove
    lp_amount = pair.balanceOf(account)
    
    # Approve the router to spend the LP tokens
    pair.approve(uniswap_router_address, lp_amount, {'from': account})

    # Get current timestamp for the deadline
    deadline = web3.eth.get_block('latest')['timestamp'] + 1000

    # Remove liquidity
    tx = uniswap_router.removeLiquidity(
        wmatic_address,
        custom_token_address,
        lp_amount,
        0,  # Min amount of WMATIC
        0,  # Min amount of custom tokens
        account.address,
        deadline,
        {'from': account}
    )

    print(f"Liquidity removed. Transaction hash: {tx.txid}")

    # Display balances after removing liquidity
    wmatic_balance = wmatic.balanceOf(account)
    custom_token_balance = custom_token.balanceOf(account)
    print(f"WMATIC balance: {wmatic_balance / 10**18} WMATIC")
    print(f"Custom token balance: {custom_token_balance / 10**18} Custom Token")
