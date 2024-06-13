require('dotenv').config();
require('@nomiclabs/hardhat-ethers');
require('@nomiclabs/hardhat-waffle');

module.exports = {
    solidity: "0.8.24",
    networks: {
        localhost: {
            url: "http://127.0.0.1:8545"
        },
        hardhat: {},
        amoy: {
            url: "https://rpc-amoy.polygon.technology",
            accounts: [process.env.PRIVATE_KEY],
            chainid: "80002"
	}
    }
};
