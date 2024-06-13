from brownie import accounts, network

def main():
    # Load the sender account using the private key
    sender = accounts.add("0xdce0ef6c16220393460052f7bc7caf1327ca24e8e185a2b6ec601ed4f79fc91a")
    
    # Define the recipient address
    recipient = "0x3Caddf9F0ea28EcCaaF3D971Db436f1f2Bf06351"
    
    # Define the amount to transfer (990 ETH)
    amount = "990 ether"
    
    # Print sender's balance before transfer
    print(f"Sender balance before transfer: {sender.balance()} wei")
    
    # Print recipient's balance before transfer
    recipient_balance_before = network.web3.eth.get_balance(recipient)
    print(f"Recipient balance before transfer: {recipient_balance_before} wei")
    
    # Transfer ETH
    tx = sender.transfer(recipient, amount)
    
    # Wait for the transaction to be mined
    tx.wait(1)
    
    # Print sender's balance after transfer
    print(f"Sender balance after transfer: {sender.balance()} wei")
    
    # Print recipient's balance after transfer
    recipient_balance_after = network.web3.eth.get_balance(recipient)
    print(f"Recipient balance after transfer: {recipient_balance_after} wei")

    print(f"Transaction hash: {tx.txid}")
