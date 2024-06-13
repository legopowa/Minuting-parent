from brownie import accounts, interface, CalFundToken, WrappedMatic, web3
from web3 import Web3

def main():
    gas_price = 5 * 10**9  # 2 gwei
    gas_limit = 500000  # Fixed gas limit
    # Load the account
    account = accounts.load('test2')

    # Load contract addresses
    with open('./uniswap_router_address.txt', 'r') as f:
        uniswap_router_address = f.read().strip()

    with open('./mintaddy.txt', 'r') as f:
        custom_token_address = f.read().strip()

    with open('./wmatic_address.txt', 'r') as f:
        wmatic_address = f.read().strip()

    # Instantiate contracts
    uniswap_router = interface.IUniswapV2Router02(uniswap_router_address)
    custom_token = CalFundToken.at(custom_token_address)
    wmatic = WrappedMatic.at(wmatic_address)

    # Define the amount to swap
    amount_token = 1234 * 10**18  # Adjust as needed

    # Approve the Uniswap Router to spend the tokens
    custom_token.approve(uniswap_router_address, amount_token, {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    print(f"Approved {amount_token / 10**18} tokens for Uniswap Router")

    # Check allowance
    allowance = custom_token.allowance(account, uniswap_router_address)
    print(f"Allowance: {allowance / 10**18} tokens")

    # Perform the swap
    path = [ wmatic.address, custom_token.address]
    try:
        uniswap_router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amount_token,
            0,  # Min amount of WMATIC to receive
            path,
            account,
            (web3.eth.get_block('latest')['timestamp'] + 1000),
            {'from': account, 'gas_price': gas_price, 'gas_limit': gas_limit}
        )
        #print(f"Swap transaction successful: {tx.txid}")
    except Exception as e:
        print(f"Swap transaction failed: {str(e)}")
    
if __name__ == "__main__":
    main()
