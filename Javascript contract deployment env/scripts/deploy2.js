require('dotenv').config();
const { ethers } = require('hardhat');
const fs = require('fs');
const path = require('path');

async function main() {
    // Setup deployer using the private key from .env
    const privateKey = process.env.PRIVATE_KEY;
    if (!privateKey) {
        throw new Error('Please set your PRIVATE_KEY in a .env file');
    }

    const provider = new ethers.providers.JsonRpcProvider();
    const deployer = new ethers.Wallet(privateKey, provider);

    console.log('Deploying contracts with the account:', deployer.address);

    // Load contract artifacts from the /contracts/ directory
    const factoryArtifactPath = path.join(__dirname, '../contracts/UniswapV2Factory.json');
    const routerArtifactPath = path.join(__dirname, '../contracts/UniswapV2Router02.json');
    const pairArtifactPath = path.join(__dirname, '../contracts/UniswapV2Pair.json');
    const wethArtifactPath = path.join(__dirname, '../contracts/WETH9.json');

    if (!fs.existsSync(factoryArtifactPath)) {
        throw new Error(`Factory artifact file not found at path: ${factoryArtifactPath}`);
    }
    if (!fs.existsSync(routerArtifactPath)) {
        throw new Error(`Router artifact file not found at path: ${routerArtifactPath}`);
    }
    if (!fs.existsSync(pairArtifactPath)) {
        throw new Error(`Pair artifact file not found at path: ${pairArtifactPath}`);
    }
    if (!fs.existsSync(wethArtifactPath)) {
        throw new Error(`WETH artifact file not found at path: ${wethArtifactPath}`);
    }

    const factoryArtifact = JSON.parse(fs.readFileSync(factoryArtifactPath));
    const routerArtifact = JSON.parse(fs.readFileSync(routerArtifactPath));
    const pairArtifact = JSON.parse(fs.readFileSync(pairArtifactPath));
    const wethArtifact = JSON.parse(fs.readFileSync(wethArtifactPath));

    // Deploy Uniswap Factory
    const Factory = new ethers.ContractFactory(factoryArtifact.abi, factoryArtifact.bytecode, deployer);
    const factory = await Factory.deploy(deployer.address);
    await factory.deployed();
    console.log('Factory deployed at:', factory.address);

    // Deploy Wrapped Ether (WETH) contract
    const Weth = new ethers.ContractFactory(wethArtifact.abi, wethArtifact.bytecode, deployer);
    const weth = await Weth.deploy();
    await weth.deployed();
    console.log('WETH deployed at:', weth.address);

    // Deploy Uniswap Router
    const Router = new ethers.ContractFactory(routerArtifact.abi, routerArtifact.bytecode, deployer);
    const router = await Router.deploy(factory.address, weth.address);
    await router.deployed();
    console.log('Router deployed at:', router.address);

    // Use pre-deployed Activity_Mint contract for ACoins
    const activityMintAddress = fs.readFileSync('Activity-Mint.txt', 'utf8').trim();
    console.log('Using pre-deployed Activity_Mint (ACoins) contract at:', activityMintAddress);

    // Create a pair
    const tx1 = await factory.createPair(activityMintAddress, weth.address);
    await tx1.wait();
    const pairAddress = await factory.getPair(activityMintAddress, weth.address);
    console.log('Pair created at:', pairAddress);

    // Save the deployed contract addresses to a file
    const addresses = {
        factory: factory.address,
        weth: weth.address,
        router: router.address,
        aCoins: activityMintAddress,
        pair: pairAddress
    };

    fs.writeFileSync('deployedAddresses.json', JSON.stringify(addresses, null, 2));

    console.log('Deployed addresses saved to deployedAddresses.json');
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
