from brownie import CalFundToken, accounts
from brownie.network.gas.strategies import GasNowStrategy

def main():
    # Load the test account
    test_account = accounts.load("test2")
    test_account2 = accounts.load("user1")
    # Load the deployed CalFundToken contract
    cal_fund_token_address = "0x06318609A0eC6F59067eB8a8Ad7D5CA46851FF67"
    token = CalFundToken.at(cal_fund_token_address)

    # Gas strategy
    gas_strategy = GasNowStrategy("fast")

    # Helper function to get the MATIC balance of an address
    def get_matic_balance(address):
        return token.getMaticBalance(address)

    # Helper function to check for DexFailure event
    def check_dex_failure(tx):
        events = tx.events
        if "DexFailure" in events:
            print(f"DexFailure event detected: {events['DexFailure']['message']}")
        else:
            print("No DexFailure event detected.")

    # Scenario 1: Mint tokens to an account with less than 1 MATIC
    print("Minting tokens to an account with less than 1 MATIC...")
    recipient = "0x13A3d668a1f04D623B2Ddf6da6C1DE2a490a8Adb"  # Replace with actual address
    mint_amount = 1000 * 10**18  # Adjust as needed

    tx = token.mint(recipient, mint_amount, {'from': test_account, 'gas_limit': '60000'})
    tx.wait(1)

    print(f"Tokens minted to {recipient}. Transaction hash: {tx.txid}")
    print(f"Recipient MATIC balance after mint: {get_matic_balance(recipient)}")

    # Check for DexFailure event
    check_dex_failure(tx)

    # Scenario 2: Transfer tokens between accounts where one or both accounts have less than 1 MATIC
    print("Transferring tokens between accounts where one or both have less than 1 MATIC...")
    sender = test_account2  # Replace with actual address
    transfer_amount = 500 * 10**18  # Adjust as needed

    tx = token.transfer(recipient, transfer_amount, {'from': sender, 'gas_limit': '60000'})
    tx.wait(1)

    print(f"Tokens transferred from {sender} to {recipient}. Transaction hash: {tx.txid}")
    print(f"Sender MATIC balance after transfer: {get_matic_balance(sender)}")
    print(f"Recipient MATIC balance after transfer: {get_matic_balance(recipient)}")

    # Check for DexFailure event
    check_dex_failure(tx)

if __name__ == "__main__":
    main()
