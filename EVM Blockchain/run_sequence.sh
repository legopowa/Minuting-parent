#!/bin/bash

# Run the reset keys script
echo "Running ./keys/resetkeys2.sh..."
./keys/resetkeys2.sh

# Check if the reset keys script was successful
if [ $? -ne 0 ]; then
  echo "resetkeys2.sh failed. Exiting."
  exit 1
fi

# Run the first Brownie script
echo "Running brownie run Deploy_boilerplate..."
brownie run Deploy_boilerplate

# Check if the first command was successful
if [ $? -ne 0 ]; then
  echo "Deploy_boilerplate failed. Exiting."
  exit 1
fi

# Change directory to the JavaScript environment
echo "Changing directory to ../Javascript contract deployment env..."
cd ../Javascript\ contract\ deployment\ env

# Run the generate_dapp_addresses.sh script
echo "Running generate_dapp_addresses.sh..."
./generate_dapp_addresses.sh

# Check if the generate_dapp_addresses.sh script was successful
if [ $? -ne 0 ]; then
  echo "generate_dapp_addresses.sh failed. Exiting."
  exit 1
fi

# Change back to the original directory
echo "Changing back to the original directory..."
cd - > /dev/null

# Run the second Brownie script
echo "Running brownie run interaction2..."
brownie run interaction2

# Check if the interaction2 script was successful
if [ $? -ne 0 ]; then
  echo "interaction2 failed. Exiting."
  exit 1
fi

echo "All commands executed successfully."
