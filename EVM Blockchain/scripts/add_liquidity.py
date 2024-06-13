from brownie import CalFundToken, WrappedMatic, accounts, interface, web3
from web3 import Web3

def main():
    account = accounts.load('test2')

    # Load addresses from files
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    with open('./coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    # Instantiate contracts
    custom_token = CalFundToken.at(custom_token_address)
    wmatic = WrappedMatic.at(wmatic_address)

    # Define the amount to add (1 ETH equivalent in this example)
    amount_wmatic = 3 * 10**18  # 3 WMATIC
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
    uniswap_router_address = "0x13B4e811C99DAA2293e56f6987De4969AbD34dc3"
    wmatic.approve(uniswap_router_address, amount_wmatic, {'from': account})
    custom_token.approve(uniswap_router_address, amount_token, {'from': account})

    # Check allowances
    wmatic_allowance = wmatic.allowance(account, uniswap_router_address)
    token_allowance = custom_token.allowance(account, uniswap_router_address)
    print(f"WMATIC allowance: {wmatic_allowance}")
    print(f"Custom token allowance: {token_allowance}")

    # Ensure sufficient allowances
    if wmatic_allowance < amount_wmatic or token_allowance < amount_token:
        raise ValueError("Insufficient token allowances to add liquidity.")

    # Interact with the Uniswap Router
    router = interface.IUniswapV2Router02(uniswap_router_address)
    tx = router.addLiquidity(
        wmatic_address,
        custom_token_address,
        amount_wmatic,
        amount_token,
        0,  # Min WMATIC amount
        0,  # Min token amount
        account.address,
        (web3.eth.get_block('latest')['timestamp'] + 1000),
        {'from': account}
    )

    print(f"Liquidity added. Transaction hash: {tx.txid}")

    # Print the pair address
    print(f"Uniswap Pair Address: {pair_address}")

if __name__ == "__main__":
    main()
