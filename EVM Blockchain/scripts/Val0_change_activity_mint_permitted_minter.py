from brownie import accounts, Activity_Mint, network

def main():
    # Load the test2 account
    test2_ = accounts.load('test2')

    # Read the contents of Activity-GameValidator.txt
    with open('Activity-GameValidator.txt', 'r') as file:
        game_validator_address = file.read().strip()

    with open('Activity-Mint.txt', 'r') as file:
        mint_address = file.read().strip()

    # Ensure we are on the correct network
    #print(f'Current network: {network.show_active()}')

    # Deploy or connect to the Activity_Mint contract
    # If the contract is already deployed, get its address. Replace `Activity_Mint_Address` with the actual contract address if it's deployed.
    activity_mint = Activity_Mint.at(mint_address)
    gas_price = 120 * 10**9  # 2 gwei in wei
    gas_limit = 30000000  # Adjust as necessary
    # Call the debugAddMinter function
    tx = activity_mint.debugAddMinter("0x5CbCE708364232bcCD3F89e01d07adA819d3502b", {'from': test2_, 'amount': gas_price, 'gas_limit': gas_limit})

    # Print transaction details
    print(f'Transaction hash: {tx.txid}')
    print(f'Transaction status: {"Success" if tx.status == 1 else "Failed"}')
    print(f'Transaction gas used: {tx.gas_used}')

