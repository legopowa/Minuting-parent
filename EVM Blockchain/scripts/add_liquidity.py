from brownie import CalFundToken, WrappedMatic, UniswapV2Router01, accounts, web3

def main():
    account = accounts.load('test2')
    gas_price = 9 * 10**9  # 10 gwei in wei
    gas_limit = 10000000  # Block gas limit in Ganache

    # Load addresses from files
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    with open('./coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()

    # Instantiate contracts
    custom_token = CalFundToken.at(custom_token_address)
    wmatic = WrappedMatic.at(wmatic_address)
    uniswap_router = UniswapV2Router01.at(uniswap_router_address)

    # Define the amount to add
    amount_wmatic = 2 * 10**18  # 3 WMATIC
    amount_token = 7500 * 10**18  # Equivalent amount of custom token

    # Check balances
    wmatic_balance = wmatic.balanceOf(account)
    token_balance = custom_token.balanceOf(account)
    print(f"WMATIC balance: {wmatic_balance}")
    print(f"Custom token balance: {token_balance}")

    # Ensure sufficient balances
    if wmatic_balance < amount_wmatic or token_balance < amount_token:
        raise ValueError("Insufficient token balances to add liquidity.")

    # Approve the Uniswap Router to spend the tokens
    wmatic.approve(uniswap_router_address, amount_wmatic, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    custom_token.approve(uniswap_router_address, amount_token, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Check allowances
    wmatic_allowance = wmatic.allowance(account, uniswap_router_address)
    token_allowance = custom_token.allowance(account, uniswap_router_address)
    print(f"WMATIC allowance: {wmatic_allowance}")
    print(f"Custom token allowance: {token_allowance}")

    # Ensure sufficient allowances
    if wmatic_allowance < amount_wmatic or token_allowance < amount_token:
        raise ValueError("Insufficient token allowances to add liquidity.")
    pair_address = custom_token.getUniswapPair()
    print(pair_address)
    # Interact with the Uniswap Router
    tx = uniswap_router.addLiquidity(
        custom_token_address,
        wmatic_address,
        amount_token,
        amount_wmatic,
        0,  # Min WMATIC amount
        0,  # Min token amount
        account.address,
        (web3.eth.get_block('latest')['timestamp'] + 1000),
        {'from': account, 'gas_limit': 1000000}
    )

    print(f"Liquidity added. Transaction hash: {tx.txid}")

    # Print the pair address
    print(f"Uniswap Pair Address: {pair_address}")

if __name__ == "__main__":
    main()
