import os
from mnemonic import Mnemonic
from brownie import accounts, Whitelist, AnonIDContract

def get_address_from_mnemonic(mnemonic):
    # This function should derive the address from the mnemonic
    return accounts.from_mnemonic(mnemonic).address

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts

    # Define gas price and gas limit
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Read the Whitelist contract address from file
    with open('CalFund-Whitelist.txt', 'r') as f:
        whitelist_address = f.read().strip()
    whitelist_contract = Whitelist.at(whitelist_address)

    # Predefined address and ID
    user_addresses_and_ids = [
        ("0x3Caddf9F0ea28EcCaaF3D971Db436f1f2Bf06351", "lego_powa")
    ]

    # Load mnemonics and derive addresses
    for i in range(1, 4):
        with open(f'mnemonic{i}.txt', 'r') as f:
            mnemonic = f.read().strip()
        address = get_address_from_mnemonic(mnemonic)
        id_part = " ".join(mnemonic.split()[:3])
        user_addresses_and_ids.append((address, id_part))

    # Whitelist each user
    for address, id_part in user_addresses_and_ids:
        tx = whitelist_contract.addAddressToWhitelist(
            address, id_part, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
        )
        print(f"Whitelisted {address} with ID {id_part}")

        # Capture and process events
        operation_results = tx.events['OperationResult']

        for event in operation_results:
            success = event['success']
            message = event['message']
            print(f"Operation Result: Success={success}, Message='{message}'")

        # Process error events if they exist
        if 'ErrorCaught' in tx.events:
            error_events = tx.events['ErrorCaught']
            for event in error_events:
                action = event['action']
                error = event['error']
                print(f"Error in action {action}: {error}")

    print("Whitelisting complete.")
