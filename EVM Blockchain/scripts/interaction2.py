from brownie import accounts, network, web3, Activity_Mint, interface
import json
import os
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables
    load_dotenv()
    gas_price = 5 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Set up the deployer account
    deployer = accounts.load('test2')
    print('Interacting with contracts using the account:', deployer.address)

    # Load the Activity_Mint address from mintaddy.txt
    with open('Activity-Mint.txt', 'r') as f:
        mint_address = f.read().strip()

    # Load deployed addresses
    with open('deployedAddresses.json') as f:
        addresses = json.load(f)

    # Load the pair address from coinpair.txt
    with open('coinpair.txt', 'r') as f:
        pair_address = f.read().strip()

    # Set up the contract objects
    ACoin = Activity_Mint.at(mint_address)
    router = interface.IUniswapV2Router02(addresses['router'])
    pair = interface.IUniswapV2Pair(pair_address)
    weth = interface.IWETH(addresses['weth'])

    # Step 1: Mint WETH
    mint_weth_tx = weth.deposit({'from': deployer, 'value': web3.to_wei(2, 'ether'), 'gas_price': gas_price, 'gas_limit': gas_limit})
    mint_weth_tx.wait(1)
    print('Minted 2 WETH')

    # Display deployer's balance
    ACoin_balance = ACoin.balanceOf(deployer.address)
    weth_balance = weth.balanceOf(deployer.address)
    print('Deployer ACoins balance:', web3.from_wei(ACoin_balance, 'ether'))
    print('Deployer WETH balance:', web3.from_wei(weth_balance, 'ether'))

    # Step 2: Add Liquidity
    aCoins_amount = web3.to_wei(7500, 'ether')  # 7500 ACoins
    weth_amount = web3.to_wei(2, 'ether')  # 2 WETH
    deadline = web3.eth.get_block('latest')['timestamp'] + (10 * 60)  # 10 minutes from the current Unix time

    # Approve tokens for liquidity addition
    ACoin.approve(router.address, aCoins_amount, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}).wait(1)
    weth.approve(router.address, weth_amount, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}).wait(1)

    add_liquidity_tx = router.addLiquidity(
        ACoin.address,
        weth.address,
        aCoins_amount,
        weth_amount,
        0,
        0,
        deployer.address,
        deadline,
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    add_liquidity_tx.wait(1)
    print('Liquidity added')

    # Step 3: Perform Swaps

    # Fetch and display reserves before the swap
    reserves = pair.getReserves()
    print('Reserves before swap:', reserves)
    print('Pair ACoins balance before swap:', web3.from_wei(reserves[0], 'ether'))
    print('Pair WETH balance before swap:', web3.from_wei(reserves[1], 'ether'))

    # Perform a swap from ACoins to WETH
    amount_in_aCoins = web3.to_wei(500, 'ether')  # 500 ACoins
    amount_out_min_weth = 0  # Accept any amount of WETH

    ACoin.approve(router.address, amount_in_aCoins, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}).wait(1)
    swap_path_aCoins_to_weth = [ACoin.address, weth.address]
    aCoins_to_weth_swap_tx = router.swapExactTokensForTokens(
        amount_in_aCoins,
        amount_out_min_weth,
        swap_path_aCoins_to_weth,
        deployer.address,
        (web3.eth.get_block('latest')['timestamp'] + (10 * 60)),
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    aCoins_to_weth_swap_tx.wait(1)
    print('ACoins to WETH swap executed')

    # Fetch and display reserves after the first swap
    reserves = pair.getReserves()
    print('Reserves after ACoins to WETH swap:', reserves)
    print('Pair ACoins balance after ACoins to WETH swap:', web3.from_wei(reserves[0], 'ether'))
    print('Pair WETH balance after ACoins to WETH swap:', web3.from_wei(reserves[1], 'ether'))

    # Perform a swap from WETH to ACoins
    amount_in_weth = web3.to_wei(0.1, 'ether')  # 0.1 WETH
    amount_out_min_aCoins = 0  # Accept any amount of ACoins

    weth.approve(router.address, amount_in_weth, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}).wait(1)
    swap_path_weth_to_aCoins = [weth.address, ACoin.address]
    weth_to_aCoins_swap_tx = router.swapExactTokensForTokens(
        amount_in_weth,
        amount_out_min_aCoins,
        swap_path_weth_to_aCoins,
        deployer.address,
        (web3.eth.get_block('latest')['timestamp'] + (10 * 60)),
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    weth_to_aCoins_swap_tx.wait(1)
    print('WETH to ACoins swap executed')

    # Fetch and display reserves after the second swap
    reserves = pair.getReserves()
    print('Reserves after WETH to ACoins swap:', reserves)
    print('Pair ACoins balance after WETH to ACoins swap:', web3.from_wei(reserves[0], 'ether'))
    print('Pair WETH balance after WETH to ACoins swap:', web3.from_wei(reserves[1], 'ether'))

    # Display deployer's new balance
    new_aCoins_balance = ACoin.balanceOf(deployer.address)
    new_weth_balance = weth.balanceOf(deployer.address)
    print('New ACoins balance:', web3.from_wei(new_aCoins_balance, 'ether'))
    print('New WETH balance:', web3.from_wei(new_weth_balance, 'ether'))

def load_dotenv():
    from dotenv import load_dotenv
    load_dotenv()

if __name__ == "__main__":
    main()
