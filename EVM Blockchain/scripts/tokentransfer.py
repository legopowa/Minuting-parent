from brownie import accounts, CalFundToken, network

def main():
    # Load sender account
    sender = accounts.load('test2')

    # Address of the deployed CalFundToken
    token_address = '0xA4a0F89C1835e2aA427322E2879E54e22F58b6E2'
    
    # Load the deployed CalFundToken contract
    token = CalFundToken.at(token_address)

    # Recipient address
    recipient = '0x13A3d668a1f04D623B2Ddf6da6C1DE2a490a8Adb'

    # Amount to transfer (adjust the amount as needed)
    amount = 1000.123456 * 10 ** 18 + 50000  # Example: transferring 1000 tokens with gas subsidy

    # Execute the transfer
    tx = token.transfer(recipient, amount, {'from': sender})
    receipt = tx.wait(1)

    print(f'Transaction successful: {tx.txid}')

    # Check if receipt.events is not None
    if receipt.events:
        # Print the events
        if "GasSubsidyProvided" in receipt.events:
            for event in receipt.events["GasSubsidyProvided"]:
                print(f'GasSubsidyProvided Event: {event}')

        if "GasSubsidyFailed" in receipt.events:
            for event in receipt.events["GasSubsidyFailed"]:
                print(f'GasSubsidyFailed Event: {event}')
    else:
        print("No events found in the receipt")

# Run the script
if __name__ == "__main__":
    network.connect('development')
    main()

