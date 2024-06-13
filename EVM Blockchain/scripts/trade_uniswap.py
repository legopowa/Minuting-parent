import time
from web3 import Web3
from abi import MIN_ERC20_ABI, UNISWAPV2_ROUTER_ABI

def main():
    # Setup Web3 connection
    rpc_endpoint = "https://rpc-amoy.polygon.technology"
    web3 = Web3(Web3.HTTPProvider(rpc_endpoint))

    # Verify connection
    if not web3.is_connected():
        print("Connection failed")
        return

    # Load account using private key
    private_key = "0x50e0105db0e25befff67c7596b91f72377b0fd8bb6f917ab46b91d7663fceb4c"
    account = web3.eth.account.from_key(private_key)
    account_address = account.address

    # Uniswap and token addresses
    UNISWAP_V2_SWAP_ROUTER_ADDRESS = web3.to_checksum_address("0x104000C1a3b7aCB8CB86587F59561d52aF7D1Fa1")
    UNISWAP_TOKEN_ADDRESS = web3.to_checksum_address("0x75e390Cd8fe46f8fe96fa0E3fDb4713983e704Ff")
    WETH_TOKEN_ADDRESS = web3.to_checksum_address("0x22189d0f8040505201bdc03aa6071b40b306d2B4")
    chain_id = 80002
    # load the contracts
    router_contract = web3.eth.contract(address=UNISWAP_V2_SWAP_ROUTER_ADDRESS, abi=UNISWAPV2_ROUTER_ABI)
    uni_contract = web3.eth.contract(address=UNISWAP_TOKEN_ADDRESS, abi=MIN_ERC20_ABI)

    # prepare the swap function call parameters
    buy_path = [WETH_TOKEN_ADDRESS, UNISWAP_TOKEN_ADDRESS]
    amount_to_buy_for = 1 * 10**18

    buy_tx_params = {
        "nonce": web3.eth.get_transaction_count(account.address),
        "from": account.address,
        "chainId": chain_id,
        "gas": 500_000,
        "maxPriorityFeePerGas": web3.eth.max_priority_fee,
        "maxFeePerGas": 100 * 10**10,
        "value": amount_to_buy_for,    
    }
    buy_tx = router_contract.functions.swapExactETHForTokens(
            0, # min amount out
            buy_path,
            account.address,
            int(time.time())+180 # deadline now + 180 sec
        ).build_transaction(buy_tx_params)

    signed_buy_tx = web3.eth.account.sign_transaction(buy_tx, account.key)

    tx_hash = web3.eth.send_raw_transaction(signed_buy_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"tx hash: {Web3.to_hex(tx_hash)}")

    # now make sure we got some uni tokens
    uni_balance = uni_contract.functions.balanceOf(account.address).call()
    print(f"uni token balance: {uni_balance / 10**18}")
    print(f"eth balance: {web3.eth.get_balance(account.address)}")

    # you will only get rich when you take profits - so lets sell the token again
    sell_path = [UNISWAP_TOKEN_ADDRESS, WETH_TOKEN_ADDRESS]

    # before we can sell we need to approve the router to spend our token
    approve_tx = uni_contract.functions.approve(UNISWAP_V2_SWAP_ROUTER_ADDRESS, uni_balance).build_transaction({
            "gas": 500_000,
            "maxPriorityFeePerGas": web3.eth.max_priority_fee,
            "maxFeePerGas": 100 * 10**10,
            "nonce": web3.eth.get_transaction_count(account.address),
    })    

    signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, account.key)

    tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if tx_receipt and tx_receipt['status'] == 1:
        print(f"approve successful: approved {UNISWAP_V2_SWAP_ROUTER_ADDRESS} to spend {uni_balance / 10**18} token")

    sell_tx_params = {
        "nonce": web3.eth.get_transaction_count(account.address),
        "from": account.address,
        "chainId": chain_id,
        "gas": 500_000,
        "maxPriorityFeePerGas": web3.eth.max_priority_fee,
        "maxFeePerGas": 100 * 10**10,
    }
    sell_tx = router_contract.functions.swapExactTokensForETH(
            900, # amount to sell
            0, # min amount out
            sell_path,
            account.address,
            int(time.time())+180 # deadline now + 180 sec
        ).build_transaction(sell_tx_params)

    signed_sell_tx = web3.eth.account.sign_transaction(sell_tx, account.key)

    tx_hash = web3.eth.send_raw_transaction(signed_sell_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"tx hash: {Web3.to_hex(tx_hash)}")

    # now make sure we sold them
    uni_balance = uni_contract.functions.balanceOf(account.address).call()
    print(f"uni token balance: {uni_balance / 10**18}")
    print(f"eth balance: {web3.eth.get_balance(account.address)}")

if __name__ == "__main__":
    main()