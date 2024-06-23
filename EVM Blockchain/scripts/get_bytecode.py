from brownie import project, network, accounts

def main():
    # Prompt the user to input the contract name
    contract_name = input("Enter the contract name: ")

    # Load the project if not already loaded
    if not project.check_for_project():
        project.load()

    # Connect to a network (e.g., development network)
    if not network.is_connected():
        network.connect('development')

    # Get the contract bytecode
    try:
        # Access the contract from the loaded project
        project_instance = project.get_loaded_projects()[0]
        contract = getattr(project_instance, contract_name)
        bytecode = contract.bytecode
        print(f"Bytecode for {contract_name}:")
        print(bytecode)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
