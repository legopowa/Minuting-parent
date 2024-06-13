from brownie import accounts, web3

def main():
    # Load the test2 account
    sender_account = accounts.load('user1')

    # Specify the recipient address
    recipient_address = "0x13A3d668a1f04D623B2Ddf6da6C1DE2a490a8Adb"

    # Specify the amount of MATIC to send (in Wei)
    amount = web3.to_wei(0.2, 'ether')  # 1 MATIC (adjust as needed)

    # Send the transaction
    tx = sender_account.transfer(recipient_address, amount)

    print(f"Transaction successful. Hash: {tx.txid}")
    print(f"Sent {amount / 10**18} MATIC to {recipient_address}")
