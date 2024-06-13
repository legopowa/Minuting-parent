from brownie import SwapTest, CalFundToken, WrappedMatic, accounts

def main():
    account = accounts.load('test2')
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 10000000  # Block gas limit in Ganache

    # Load addresses from files
    with open('./swap_test_address.txt', 'r') as f:
        swap_test_address = f.read().strip()
    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()
    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()

    # Instantiate the SwapTest, CalFundToken, and WrappedMatic contracts
    swap_test = SwapTest.at(swap_test_address)
    custom_token = CalFundToken.at(custom_token_address)
    wmatic = WrappedMatic.at(wmatic_address)

    # Define the amount to swap
    token_amount = 500 * 10**18  # 1 token
    token_amt_with_fee = token_amount * 1.1

    # Approve the SwapTest contract to spend the tokens
    custom_token.approve(swap_test_address, token_amt_with_fee, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Approve the Uniswap Router to spend the tokens
    custom_token.approve(uniswap_router_address, token_amt_with_fee, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Perform the token swap
    tx = swap_test.swapExactTokensForTokens(token_amount, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    tx.wait(1)
    print(f"Swap transaction hash: {tx.txid}")

    # Capture and print emitted events
    if "SwapStarted" in tx.events:
        print(f"SwapStarted: {tx.events['SwapStarted']}")
    if "SwapSuccess" in tx.events:
        print(f"SwapSuccess: {tx.events['SwapSuccess']}")
    if "SwapFailed" in tx.events:
        print(f"SwapFailed: {tx.events['SwapFailed']}")

if __name__ == "__main__":
    main()
