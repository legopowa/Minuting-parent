from brownie import CalFundToken, accounts
from brownie.network.gas.strategies import GasNowStrategy

def main():
    # Load accounts
    test_account = accounts.load("test2")
    sender = accounts.load("user1")
    metamask = "0x13A3d668a1f04D623B2Ddf6da6C1DE2a490a8Adb"

    # Load contract
    with open('./mintaddy.txt', 'r') as f:
        cal_fund_token_address = f.read().strip()
    token = CalFundToken.at(cal_fund_token_address)

    gas_price = 2 * 10**9  # 2 gwei
    gas_limit = 500000  # Fixed gas limit

    # Helper functions
    def get_matic_balance(address):
        return token.getMaticBalance(address)

    def check_events(tx):
        events = tx.events
        if "GasSubsidyFailed" in events:
            print(f"GasSubsidyFailed event: {events['GasSubsidyFailed']}")
        if "GasSubsidyProvided" in events:
            print(f"GasSubsidyProvided event: {events['GasSubsidyProvided']}")
        if "GasSubsidyCalculated" in events:
            print(f"GasSubsidyCalculated event: {events['GasSubsidyCalculated']}")
        if "GasLimitCalculated" in events:
            print(f"GasLimitCalculated event: {events['GasLimitCalculated']}")
        if "TokensSwappedForWMatic" in events:
            print(f"TokensSwappedForWMatic event: {events['TokensSwappedForWMatic']}")
        if "TokensApproved" in events:
            print(f"TokensApproved event: {events['TokensApproved']}")
        if "TokensSwapped" in events:
            print(f"TokensSwapped event: {events['TokensSwapped']}")
        if "WmaticUnwrapped" in events:
            print(f"WmaticUnwrapped event: {events['WmaticUnwrapped']}")
        if "MaticSent" in events:
            print(f"MaticSent event: {events['MaticSent']}")

    # Mint tokens
    print("Minting tokens...")
    mint_amount = 2500.1234561 * 10**18
    print(f"Test_account MATIC balance before mint: {get_matic_balance(test_account)}")
    tx = token.mint(sender, mint_amount, {'from': test_account, 'gas_price': gas_price, 'gas_limit': gas_limit})
    print(f"Tokens minted to {sender}. Transaction hash: {tx.txid}")
    print(f"Recipient MATIC balance after mint: {get_matic_balance(sender)}")
    print(f"Test_account MATIC balance after mint: {get_matic_balance(test_account)}")
    check_events(tx)

    # Transfer tokens
    print("Transferring tokens...")
    transfer_amount = 2000.1234561 * 10**18
    print(f"Recipient MATIC balance before transfer: {get_matic_balance(metamask)}")
    tx = token.transfer(metamask, transfer_amount, {'from': sender, 'gas_price': gas_price, 'gas_limit': gas_limit})
    print(f"Tokens transferred from {sender} to {metamask}. Transaction hash: {tx.txid}")
    print(f"Sender MATIC balance after transfer: {get_matic_balance(sender)}")
    print(f"Recipient MATIC balance after transfer: {get_matic_balance(metamask)}")
    check_events(tx)

if __name__ == "__main__":
    main()
