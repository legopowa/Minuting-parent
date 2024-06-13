from brownie import accounts, interface, chain

def main():
    # Load accounts
    account = accounts.load("test2")
    
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
    custom_token = interface.IERC20(custom_token_address)
    wmatic = interface.IERC20(wmatic_address)
    router = interface.IUniswapV2Router02(uniswap_router_address)
    
    # Define swap amounts
    token_amount_to_swap = 100 * 10**18  # Amount of custom token to swap
    wmatic_amount_to_swap = 1 * 10**18  # Amount of WMATIC to swap
    
    # Approve the router to spend the tokens
    custom_token.approve(uniswap_router_address, token_amount_to_swap, {'from': account})
    wmatic.approve(uniswap_router_address, wmatic_amount_to_swap, {'from': account})
    
    # Perform the token to WMATIC swap
    token_to_wmatic_path = [custom_token_address, wmatic_address]
    deadline = chain.time() + 600  # 10 minutes from now
    router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        token_amount_to_swap,
        0,
        token_to_wmatic_path,
        account.address,
        deadline,
        {'from': account}
    )
    
    print("Swap from custom token to WMATIC completed.")
    
    # Perform the WMATIC to token swap
    wmatic_to_token_path = [wmatic_address, custom_token_address]
    router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        wmatic_amount_to_swap,
        0,
        wmatic_to_token_path,
        account.address,
        deadline,
        {'from': account}
    )
    
    print("Swap from WMATIC to custom token completed.")

if __name__ == "__main__":
    main()
