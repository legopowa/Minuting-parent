from brownie import accounts, GameValidator, network, web3


def main():
    # Load the test2 account
    test2_ = accounts.load('test2')

    # Read the GameValidator contract address from file
    with open('Activity-GameValidator.txt', 'r') as file:
        game_validator_address = file.read().strip()

    # Connect to the GameValidator contract
    game_validator = GameValidator.at(game_validator_address)

    # Define the list of player names
    player_names = ["legopowa", "Player1", "Player2", "Player3"]
    gas_price = web3.to_wei('2', 'gwei')
    gas_limit = 3000000
    # Call the getValidRewardAddressesByNames function
    reward_addresses = game_validator.getValidRewardAddressesByNames(player_names, {'from': test2_, 'gas_price': gas_price, 'gas_limit': gas_limit})

    # Print the reward addresses
    print(f'Reward Addresses for players {player_names}: {reward_addresses}')
    print(reward_addresses.events)
