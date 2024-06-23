from brownie import accounts, network, web3, CalFundToken, interface
import json
import os
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables
    load_dotenv()

    # Set up the deployer and user accounts
    deployer = accounts.load('test2')
    user1 = accounts.load('user1')
    metamask_address = '0x13A3d668a1f04D623B2Ddf6da6C1DE2a490a8Adb'
    
    print('Interacting with contracts using the deployer account:', deployer.address)
    print('Interacting with contracts using the user1 account:', user1.address)

    # Load the CalFundToken address from mintaddy.txt
    with open('mintaddy.txt', 'r') as f:
        cal_address = f.read().strip()

    # Load deployed addresses
    with open('deployedAddresses.json') as f:
        addresses = json.load(f)

    # Load the pair address from coinpair.txt
    with open('coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    # Set up the contract objects
    cal = CalFundToken.at(cal_address)
    router = interface.IUniswapV2Router02(addresses['router'])
    pair = interface.IUniswapV2Pair(pair_address)
    weth = interface.IWETH(addresses['weth'])

    # Display initial ETH balances
    print('Deployer initial ETH balance:', web3.from_wei(web3.eth.get_balance(deployer.address), 'ether'))
    print('User1 initial ETH balance:', web3.from_wei(web3.eth.get_balance(user1.address), 'ether'))
    print('MetaMask address initial ETH balance:', web3.from_wei(web3.eth.get_balance(metamask_address), 'ether'))

    # Mint tokens to user1 with eth subsidy
    mint_amount = web3.to_wei(1000.1234561, 'ether')  # Mint 1000 tokens with eth subsidy
    mint_tx = cal.mint(user1.address, mint_amount, {'from': deployer})
    mint_tx.wait(1)
    print('Minted tokens to user1')

    # Capture and print events from mint transaction
    capture_and_print_events(mint_tx)

    # Display balances after minting
    print('Deployer ETH balance after mint:', web3.from_wei(web3.eth.get_balance(deployer.address), 'ether'))
    print('User1 ETH balance after mint:', web3.from_wei(web3.eth.get_balance(user1.address), 'ether'))
    print('MetaMask address ETH balance after mint:', web3.from_wei(web3.eth.get_balance(metamask_address), 'ether'))

    # Perform a transfer from user1 to MetaMask address with eth subsidy
    transfer_amount = web3.to_wei(500.1234561, 'ether')  # Transfer 500 tokens with eth subsidy
    transfer_tx = cal.transfer(metamask_address, transfer_amount, {'from': user1})
    transfer_tx.wait(1)
    print('Transferred tokens from user1 to MetaMask address')

    # Capture and print events from transfer transaction
    capture_and_print_events(transfer_tx)

    # Display balances after transfer
    print('Deployer ETH balance after transfer:', web3.from_wei(web3.eth.get_balance(deployer.address), 'ether'))
    print('User1 ETH balance after transfer:', web3.from_wei(web3.eth.get_balance(user1.address), 'ether'))
    print('MetaMask address ETH balance after transfer:', web3.from_wei(web3.eth.get_balance(metamask_address), 'ether'))

    # Swap CAL for WETH to provide ETH subsidy
    eth_amount = web3.to_wei(0.1, 'ether')  # 0.1 WETH
    token_amount = 800 * 10**18  # 800 CAL with 18 decimals

    # Approve the router to spend the tokens
    cal.approve(router.address, token_amount, {'from': deployer}).wait(1)
    print('Approved router to spend CAL tokens')

    # Fetch and display pair reserves before the swap
    reserves = pair.getReserves()
    print(f'Pair reserves before swap: CAL={reserves[0]}, WETH={reserves[1]}')

    # Perform the swap
    path = [cal_address, weth.address]
    try:
        swap_tx = router.swapTokensForExactTokens(
            eth_amount,
            token_amount,
            path,
            deployer.address,
            (web3.eth.get_block('latest').timestamp + (10 * 60)),
            {'from': deployer, 'gas_limit': 1000000}
        )
        swap_tx.wait(1)
        print('Swapped CAL for WETH to provide ETH subsidy')
    except Exception as e:
        print(f'Error during swap: {e}')

    # Capture and print events from swap transaction
    capture_and_print_events(swap_tx)

    # Fetch and display pair reserves after the swap
    reserves = pair.getReserves()
    print(f'Pair reserves after swap: CAL={reserves[0]}, WETH={reserves[1]}')

def capture_and_print_events(tx):
    # Check if tx.events is not None
    if tx.events:
        # Print the events
        if "EthSubsidyProvided" in tx.events:
            for event in tx.events["EthSubsidyProvided"]:
                print(f'EthSubsidyProvided Event: {event}')

        if "EthSubsidyFailed" in tx.events:
            for event in tx.events["EthSubsidyFailed"]:
                print(f'EthSubsidyFailed Event: {event}')

        if "SwapSucceeded" in tx.events:
            for event in tx.events["SwapSucceeded"]:
                print(f'SwapSucceeded Event: {event}')

        if "SwapFailed" in tx.events:
            for event in tx.events["SwapFailed"]:
                print(f'SwapFailed Event: {event}')

        if "ApprovalSucceeded" in tx.events:
            for event in tx.events["ApprovalSucceeded"]:
                print(f'ApprovalSucceeded Event: {event}')

        if "ApprovalFailed" in tx.events:
            for event in tx.events["ApprovalFailed"]:
                print(f'ApprovalFailed Event: {event}')
    else:
        print("No events found in the receipt")

if __name__ == "__main__":
    main()
