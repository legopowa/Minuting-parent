coding env is in node_modules
To run, do npx hardhat run ./scripts/deploy.js, --network localhost, then do same for ./scripts/interaction.js
generated uniswap addresses are in deployedAddresses.json, including functional UniswapV2Factory / router, two working coins and their coin pair
set private key in .env 



# Sample Hardhat Project

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a Hardhat Ignition module that deploys that contract.

Try running some of the following tasks:

```shell
npx hardhat help
npx hardhat test
REPORT_GAS=true npx hardhat test
npx hardhat node
npx hardhat ignition deploy ./ignition/modules/Lock.js
```


