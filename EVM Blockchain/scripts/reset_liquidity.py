from brownie import accounts, interface, Contract, web3
import time

def main():
    # Comment out network.connect
    # network.connect('development')

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

    # Call the removeLiquidity function to remove all existing liquidity
    tx_remove = router.removeLiquidity(
        wmatic_address,
        custom_token_address,
        liquidity,
        0,  # Minimum amount of WMATIC to receive
        0,  # Minimum amount of custom tokens to receive
        account.address,
        (web3.eth.get_block('latest')['timestamp'] + 1000),
        {'from': account}
    )

    print(f"Liquidity removed. Transaction hash: {tx_remove.txid}")

    # Optional: Add new liquidity to reset the pool
    amount_wmatic = 3 * 10**18  # 3 WMATIC
    amount_token = 7500 * 10**18  # Equivalent amount of custom token

    # Check balances
    wmatic = Contract.from_abi("WMATIC", wmatic_address, interface.IERC20.abi)
    custom_token = Contract.from_abi("CustomToken", custom_token_address, interface.IERC20.abi)

    wmatic_balance = wmatic.balanceOf(account)
    token_balance = custom_token.balanceOf(account)
    print(f"WMATIC balance: {wmatic_balance}")
    print(f"Custom token balance: {token_balance}")

    # Ensure sufficient balances for new liquidity
    if wmatic_balance < amount_wmatic or token_balance < amount_token:
        raise ValueError("Insufficient token balances to add new liquidity.")

    # Approve the Uniswap Router to spend the new tokens
    wmatic.approve(uniswap_router_address, amount_wmatic, {'from': account})
    custom_token.approve(uniswap_router_address, amount_token, {'from': account})

    # Check allowances for new liquidity
    wmatic_allowance = wmatic.allowance(account, uniswap_router_address)
    token_allowance = custom_token.allowance(account, uniswap_router_address)
    print(f"WMATIC allowance: {wmatic_allowance}")
    print(f"Custom token allowance: {token_allowance}")

    # Ensure sufficient allowances for new liquidity
    if wmatic_allowance < amount_wmatic or token_allowance < amount_token:
        raise ValueError("Insufficient token allowances to add new liquidity.")

    # Call the addLiquidity function to add new liquidity
    tx_add = router.addLiquidity(
        wmatic_address,
        custom_token_address,
        amount_wmatic,
        amount_token,
        0,  # Minimum amount of WMATIC to add
        0,  # Minimum amount of custom tokens to add
        account.address,
        (web3.eth.get_block('latest')['timestamp'] + 1000),
        {'from': account}
    )

    print(f"New liquidity added. Transaction hash: {tx_add.txid}")

    # Periodically show WMATIC balance
    show_wmatic_balance_periodically(wmatic, account)

def show_wmatic_balance_periodically(wmatic, account, interval=10):
    try:
        while True:
            balance = wmatic.balanceOf(account)
            print(f"Current WMATIC balance: {balance}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped periodic balance check.")

if __name__ == "__main__":
    main()
