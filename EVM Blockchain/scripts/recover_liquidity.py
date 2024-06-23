from brownie import accounts, interface, network, web3
import json
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Set up the deployer account
    deployer = accounts.load('test2')
    print('Interacting with contracts using the account:', deployer.address)

    # Load addresses
    with open('deployedAddresses.json') as f:
        addresses = json.load(f)

    # Load contract objects
    router = interface.IUniswapV2Router02(addresses['router'])
    pair = interface.IUniswapV2Pair(addresses['pair'])
    wmatic = interface.IWETH(addresses['weth'])

    # Get the pair address and LP token balance
    lp_balance = pair.balanceOf(deployer.address)
    print(f'Deployer LP token balance: {web3.from_wei(lp_balance, "ether")}')

    # Approve the router to spend the LP tokens
    pair.approve(router.address, lp_balance, {'from': deployer}).wait(1)
    print('Approved router to spend LP tokens')

    # Remove liquidity
    token0 = pair.token0()
    token1 = pair.token1()
    deadline = web3.eth.get_block('latest').timestamp + 300  # 5 minutes from the current block

    tx = router.removeLiquidity(
        token0,
        token1,
        lp_balance,
        0,  # Minimum amount of token0 to receive
        0,  # Minimum amount of token1 to receive
        deployer.address,
        deadline,
        {'from': deployer}
    )
    tx.wait(1)
    print('Liquidity removed')

    # Display new balances
    token0_contract = interface.IERC20(token0)
    token1_contract = interface.IERC20(token1)
    token0_balance = token0_contract.balanceOf(deployer.address)
    token1_balance = token1_contract.balanceOf(deployer.address)

    print(f'Deployer token0 balance: {web3.from_wei(token0_balance, "ether")}')
    print(f'Deployer token1 balance: {web3.from_wei(token1_balance, "ether")}')

if __name__ == "__main__":
    main()
