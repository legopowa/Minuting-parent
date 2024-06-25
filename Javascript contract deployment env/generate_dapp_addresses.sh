#!/bin/bash

# Run the deploy script
npx hardhat run ./scripts/deploy.js --network localhost

# Check if the deploy script was successful
if [ $? -ne 0 ]; then
    echo "Deployment failed. Exiting."
    exit 1
fi

# Define the source and destination paths
SOURCE_PATH="./deployedAddresses.json"
DESTINATION_PATH="../EVM Blockchain/deployedAddresses.json"

# Check if the deployedAddresses.json file exists
if [ ! -f "$SOURCE_PATH" ]; then
    echo "deployedAddresses.json file not found. Exiting."
    exit 1
fi

# Move the file to the destination directory
mv "$SOURCE_PATH" "$DESTINATION_PATH"

# Check if the move was successful
if [ $? -eq 0 ]; then
    echo "File successfully moved to $DESTINATION_PATH"
else
    echo "Failed to move the file. Exiting."
    exit 1
fi
