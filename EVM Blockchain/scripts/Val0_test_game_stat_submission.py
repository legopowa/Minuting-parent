from brownie import accounts, network, web3, GameValidator, Activity_Mint
from pathlib import Path
from web3 import Web3
import json
import time

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
    print(f"Using sender account: {sender.address}")

    # Load mnemonics and generate accounts
    mnemonics = ['mnemonic1.txt', 'mnemonic2.txt', 'mnemonic3.txt']
    recipient_accounts = [generate_account_from_mnemonic(load_mnemonic(mnemonic)) for mnemonic in mnemonics]
    recipient_addresses = [account.address for account in recipient_accounts]

    # Load the GameValidator contract
    with open('Activity-GameValidator.txt', 'r') as file:
        contract_address = file.read().strip()


    with open('Activity-Mint.txt', 'r') as file:
        mint_address = file.read().strip()



    _contract = GameValidator.at(contract_address)
    mint_contract = Activity_Mint.at(mint_address)

    gas_price = web3.to_wei('2', 'gwei')
    gas_limit = 3000000

    while True:
        serverPlayersLists = [
            {
                "serverIP": "172.93.101.194:27015",
                "playerNames": ["legopowa"]
            },
            {
                "serverIP": "63.143.56.124:27015",
                "playerNames": ["Player1", "Player2", "Player3"]
            },
            {
                "serverIP": "172.233.224.83:27015",
                "playerNames": ["PlayerE", "PlayerF"]
            }
        ]         
        formatted_lists = [
            (item["serverIP"], item["playerNames"]) for item in serverPlayersLists
        ]

        for address in recipient_addresses:
            tx = _contract.submitPlayerListStepTwo(
                formatted_lists,
                address,
                1,
                {'from': sender, 'gas_price': gas_price, 'gas_limit': gas_limit}
            )
            tx.wait(1)
            print(f"Submitted player list for address: {address}. Transaction hash: {tx.txid}")

        time.sleep(30)  # Adjust the sleep time as needed

        # Fetch and display balances
        for account in recipient_accounts:
            balance = mint_contract.balanceOf(account)
            print(f"Balance of {account.address}: {web3.from_wei(balance, 'ether')} ACoins")

        sender_balance = mint_contract.balanceOf(sender)
        print(f"Balance of sender {sender.address}: {web3.from_wei(sender_balance, 'ether')} ACoins")

if __name__ == "__main__":
    main()
