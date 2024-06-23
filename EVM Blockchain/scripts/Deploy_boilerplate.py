import os
from brownie import project, network, accounts

def main():
    # Load the deployer account
    deployer = accounts.load('test2')  # Make sure 'test2' is added to Brownie accounts

    # Define gas price and gas limit
    gas_price = 2 * 10**9  # 2 gwei in wei
    gas_limit = 3000000  # Adjust as necessary

    # Ensure the correct network is selected
    # network.connect('development')

    # List of scripts to run in sequence
    scripts = [
        "1_CalFund_LamportBase2_deploy",
        "2_CalFund_AnonIDContract_deploy",
        "3_CalFund_Whitelist_deploy",
        "4_Activity_LamportBase2_deploy",
        "5_Activity_Mint_deploy",
        "6_Activity_PlayerDatabase_deploy",
        "7_Activity_PlayerOnboardContract_deploy",
        "8_Activity_Validator_deploy",
        "9_AnonID_makethirdandfourthmasterkey",
        "10_AnonID_Grant_PlayerDatabase_Contract",
        "11_AnonID_Grant_Whitelist_Contract",
        "12_AnonID_Whitelist_MakeUsers",
        "13_AnonID_Whitelist_AddUsers",
        "14_Activity_makethirdandfourthmasterkey",
        "15_Activity_PlayerDatabase_Grant_GameValidator",
        "16_Activity_PlayerDatabase_Grant_Onramp",
        "17_Activity_Onboard_Test_Player_and_Validators"
        
    ]

    # Run each script in sequence
    for script in scripts:
        print(f"Running {script}...")
        project.run(script)
        print(f"Finished running {script}")

    print("All scripts have been executed.")
