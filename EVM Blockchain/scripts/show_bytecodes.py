from brownie import project

def main():
    proj = project.load('.')
    proj.load_config()
    for contract_name in proj:
        contract = proj[contract_name]
        print(f"Contract: {contract_name}")
        print("Bytecode:", contract.bytecode)
        print("Deployed Bytecode:", contract.deployed_bytecode)
        print('-' * 80)

if __name__ == "__main__":
    main()
