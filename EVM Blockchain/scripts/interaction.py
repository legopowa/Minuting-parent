from brownie import accounts, network, web3, CalFundToken, interface
import json
import os
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables
    load_dotenv()
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary
    # Set up the deployer account
    deployer = accounts.load('test2')
    print('Interacting with contracts using the account:', deployer.address)

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

    # Mint WETH
    # mint_weth_tx = weth.deposit({'from': deployer, 'value': web3.to_wei(2, 'ether')})
    # mint_weth_tx.wait(1)
    # print('Minted 2 WETH')

    # Display deployer's balance
    cal_balance = cal.balanceOf(deployer.address)
    weth_balance = weth.balanceOf(deployer.address)
    print('Deployer CAL balance:', web3.from_wei(cal_balance, 'ether'))
    print('Deployer WETH balance:', web3.from_wei(weth_balance, 'ether'))

    # Add liquidity (commented out)
    # cal_amount = web3.to_wei(7500, 'ether')  # 7500 CAL
    # weth_amount = web3.to_wei(2, 'ether')  # 2 WETH
    # deadline = web3.eth.get_block('latest').timestamp + (10 * 60)  # 10 minutes from the current Unix time

    # Approve tokens for liquidity addition (commented out)
    # cal.approve(router.address, cal_amount, {'from': deployer}).wait(1)
    # weth.approve(router.address, weth_amount, {'from': deployer}).wait(1)

    # add_liquidity_tx = router.addLiquidity(
    #     cal.address,
    #     weth.address,
    #     cal_amount,
    #     weth_amount,
    #     0,
    #     0,
    #     deployer.address,
    #     deadline,
    #     {'from': deployer, 'gas_limit': 1000000}
    # )
    # add_liquidity_tx.wait(1)
    # print('Liquidity added')

    # Fetch and display reserves before the swap
    reserves = pair.getReserves()
    print('Reserves before swap:', reserves)
    print('Pair CAL balance before swap:', web3.from_wei(reserves[0], 'ether'))
    print('Pair WETH balance before swap:', web3.from_wei(reserves[1], 'ether'))

    # Perform a swap from CAL to WETH
    amount_in_cal = web3.to_wei(500, 'ether')  # 500 CAL
    amount_out_min_weth = 0  # Accept any amount of WETH

    cal.approve(router.address, amount_in_cal, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}).wait(1)
    swap_path_cal_to_weth = [cal.address, weth.address]
    cal_to_weth_swap_tx = router.swapExactTokensForTokens(
        amount_in_cal,
        amount_out_min_weth,
        swap_path_cal_to_weth,
        deployer.address,
        (web3.eth.get_block('latest').timestamp + (10 * 60)),
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    cal_to_weth_swap_tx.wait(1)
    print('CAL to WETH swap executed')

    # Fetch and display reserves after the first swap
    reserves = pair.getReserves()
    print('Reserves after CAL to WETH swap:', reserves)
    print('Pair CAL balance after CAL to WETH swap:', web3.from_wei(reserves[0], 'ether'))
    print('Pair WETH balance after CAL to WETH swap:', web3.from_wei(reserves[1], 'ether'))

    # Perform a swap from WETH to CAL
    amount_in_weth = web3.to_wei(0.1, 'ether')  # 0.2 WETH
    amount_out_min_cal = 0  # Accept any amount of CAL

    weth.approve(router.address, amount_in_weth, {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}).wait(1)
    swap_path_weth_to_cal = [weth.address, cal.address]
    weth_to_cal_swap_tx = router.swapExactTokensForTokens(
        amount_in_weth,
        amount_out_min_cal,
        swap_path_weth_to_cal,
        deployer.address,
        (web3.eth.get_block('latest').timestamp + (10 * 60)),
        {'from': deployer, 'gas_price': gas_price, 'gas_limit': gas_limit}
    )
    weth_to_cal_swap_tx.wait(1)
    print('WETH to CAL swap executed')

    # Fetch and display reserves after the second swap
    reserves = pair.getReserves()
    print('Reserves after WETH to CAL swap:', reserves)
    print('Pair CAL balance after WETH to CAL swap:', web3.from_wei(reserves[0], 'ether'))
    print('Pair WETH balance after WETH to CAL swap:', web3.from_wei(reserves[1], 'ether'))

    # Display deployer's new balance
    new_cal_balance = cal.balanceOf(deployer.address)
    new_weth_balance = weth.balanceOf(deployer.address)
    print('New CAL balance:', web3.from_wei(new_cal_balance, 'ether'))
    print('New WETH balance:', web3.from_wei(new_weth_balance, 'ether'))

def load_dotenv():
    from dotenv import load_dotenv
    load_dotenv()
