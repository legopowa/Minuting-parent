import json
from brownie import accounts, web3, CalFundToken, Contract

def main():
    gas_price = 9 * 10**9  # 9 gwei in wei
    gas_limit = 1000000  # Block gas limit in Ganache

    # Load deployer account
    deployer = accounts.load("test2")
    print('Deploying contracts with the account:', deployer.address)

    # Fund the deployer account if needed (skip if already funded)
    # Example of funding the account from Ganache's default accounts
    #if deployer.balance() < gas_price * gas_limit:
    #    ganache_account = accounts[0]
    #    ganache_account.transfer(deployer, "10 ether")

    # Load contract artifacts from the /contracts/ directory
    with open('contracts/UniswapV2Factory.json') as f:
        factory_artifact = json.load(f)
    with open('contracts/UniswapV2Router02.json') as f:
        router_artifact = json.load(f)
    with open('contracts/WETH9.json') as f:
        weth_artifact = json.load(f)

    # Deploy Uniswap Factory
    factory_contract = web3.eth.contract(
        abi=factory_artifact['abi'],
        bytecode=factory_artifact['bytecode']
    )
    factory_txn = factory_contract.constructor().transact({'from': deployer.address, 'gasPrice': gas_price, 'gas': gas_limit})
    factory_receipt = web3.eth.wait_for_transaction_receipt(factory_txn)
    factory_address = factory_receipt.contractAddress
    print('Factory deployed at:', factory_address)

    # Deploy Wrapped Ether (WETH) contract
    weth_contract = web3.eth.contract(
        abi=weth_artifact['abi'],
        bytecode=weth_artifact['bytecode']
    )
    weth_txn = weth_contract.constructor().transact({'from': deployer.address, 'gasPrice': gas_price, 'gas': gas_limit})
    weth_receipt = web3.eth.wait_for_transaction_receipt(weth_txn)
    weth_address = weth_receipt.contractAddress
    print('WETH deployed at:', weth_address)

    # Deploy Uniswap Router
    router_contract = web3.eth.contract(
        abi=router_artifact['abi'],
        bytecode=router_artifact['bytecode']
    )
    router_txn = router_contract.constructor(factory_address, weth_address).transact({'from': deployer.address, 'gasPrice': gas_price, 'gas': gas_limit})
    router_receipt = web3.eth.wait_for_transaction_receipt(router_txn)
    router_address = router_receipt.contractAddress
    print('Router deployed at:', router_address)

    # Deploy CalFundToken
    cal = CalFundToken.deploy(deployer.address, {'from': deployer})
    print('CalFundToken deployed at:', cal.address)

    # Create a pair
    factory_contract_instance = web3.eth.contract(address=factory_address, abi=factory_artifact['abi'])
    tx1 = factory_contract_instance.functions.createPair(cal.address, weth_address).transact({'from': deployer.address, 'gasPrice': gas_price, 'gas': gas_limit})
    web3.eth.wait_for_transaction_receipt(tx1)
    pair_address = factory_contract_instance.functions.getPair(cal.address, weth_address).call()
    print('Pair created at:', pair_address)

    # Save the deployed contract addresses to a file
    addresses = {
        'factory': factory_address,
        'weth': weth_address,
        'router': router_address,
        'cal': cal.address,
        'pair': pair_address
    }

    with open('deployedAddresses.json', 'w') as f:
        json.dump(addresses, f, indent=2)

    print('Deployed addresses saved to deployedAddresses.json')
