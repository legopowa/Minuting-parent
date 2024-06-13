from brownie import accounts, web3

def main():
    # Connect to your Ganache instance
    ganache_url = "http://127.0.0.1:8545"
    web3.provider = web3.HTTPProvider(ganache_url)

    # Sender's private key and address
    sender_private_key = "0xc4964663743add43540574f342fea30f21adc09510bf2f71e18057795f2e0f51"
    sender_account = web3.eth.account.from_key(sender_private_key)

    # Load recipient address (Brownie test2 account)
    recipient_account = accounts.load('test2')

    # Amount to send (999 ETH in Wei)
    amount = web3.to_wei(999, 'ether')

    # Get the nonce
    nonce = web3.eth.get_transaction_count(sender_account.address)

    # Create the transaction
    tx = {
        'nonce': nonce,
        'to': recipient_account.address,
        'value': amount,
        'gas': 21000,
        'gasPrice': web3.to_wei('50', 'gwei')
    }

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, sender_private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Get the transaction hash
    print(f"Transaction hash: {tx_hash.hex()}")
