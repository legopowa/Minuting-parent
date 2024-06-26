from brownie import accounts, network, web3
from pathlib import Path

def load_mnemonic(mnemonic_file):
    mnemonic_path = Path(mnemonic_file)
    if not mnemonic_path.is_file():
        raise Exception(f"Can't find {mnemonic_path}")
    
    with open(mnemonic_path, "r") as file:
        return file.read().strip()

def generate_account_from_mnemonic(mnemonic):
    account = accounts.from_mnemonic(mnemonic, count=1)
    return account

def main():
    # Load the test2 account
    sender = accounts.load('test2')
    print(f"Sending ETH from: {sender.address}")

    # Load mnemonics and generate accounts
    mnemonics = ['mnemonic1.txt', 'mnemonic2.txt', 'mnemonic3.txt']
    recipients = [generate_account_from_mnemonic(load_mnemonic(mnemonic)) for mnemonic in mnemonics]

    # Amount to send (2 ETH)
    amount = web3.to_wei(2, 'ether')
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Send 2 ETH to each recipient
    for recipient in recipients:
        tx = sender.transfer(recipient.address, amount, gas_price=gas_price, gas_limit=gas_limit)
        print(f"Sent 2 ETH to {recipient.address}. Transaction hash: {tx.txid}")

if __name__ == "__main__":
    main()
