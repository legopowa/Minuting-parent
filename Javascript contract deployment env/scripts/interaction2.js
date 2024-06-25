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

    console.log('Interacting with contracts using the account:', deployer.address);

    // Load deployed addresses
    const addresses = JSON.parse(fs.readFileSync('deployedAddresses.json'));

    const ActivityMint = await ethers.getContractFactory('Activity_Mint');
    const aCoins = ActivityMint.attach(addresses.aCoins);

    const wethArtifactPath = path.join(__dirname, '../contracts/WETH9.json');
    const routerArtifactPath = path.join(__dirname, '../contracts/UniswapV2Router02.json');
    const pairArtifactPath = path.join(__dirname, '../contracts/UniswapV2Pair.json');

    const wethArtifact = JSON.parse(fs.readFileSync(wethArtifactPath));
    const routerArtifact = JSON.parse(fs.readFileSync(routerArtifactPath));
    const pairArtifact = JSON.parse(fs.readFileSync(pairArtifactPath));

    const weth = new ethers.Contract(addresses.weth, wethArtifact.abi, deployer);
    const router = new ethers.Contract(addresses.router, routerArtifact.abi, deployer);
    const pair = new ethers.Contract(addresses.pair, pairArtifact.abi, deployer);

    // Mint WETH
    const mintWethTx = await weth.deposit({ value: ethers.utils.parseUnits('2', 18) });
    await mintWethTx.wait();
    console.log('Minted 2 WETH');

    // Display deployer's balance
    const aCoinsBalance = await aCoins.balanceOf(deployer.address);
    const wethBalance = await weth.balanceOf(deployer.address);
    console.log('Deployer ACoins balance:', ethers.utils.formatUnits(aCoinsBalance, 18));
    console.log('Deployer WETH balance:', ethers.utils.formatUnits(wethBalance, 18));

    // Add liquidity
    const aCoinsAmount = ethers.utils.parseUnits('7500', 18); // 7500 ACoins
    const wethAmount = ethers.utils.parseUnits('2', 18); // 2 WETH
    const deadline = Math.floor(Date.now() / 1000) + (10 * 60); // 10 minutes from the current Unix time

    // Approve tokens for liquidity addition
    await aCoins.approve(router.address, aCoinsAmount).then(tx => tx.wait());
    await weth.approve(router.address, wethAmount).then(tx => tx.wait());

    const addLiquidityTx = await router.addLiquidity(
        aCoins.address,
        weth.address,
        aCoinsAmount,
        wethAmount,
        0,
        0,
        deployer.address,
        deadline,
        { gasLimit: ethers.utils.hexlify(1000000) }
    );
    await addLiquidityTx.wait();
    console.log('Liquidity added');

    // Fetch and display reserves before the swap
    let reserves = await pair.getReserves();
    console.log('Reserves before swap:', reserves);
    console.log('Pair ACoins balance before swap:', ethers.utils.formatUnits(reserves._reserve1, 18));
    console.log('Pair WETH balance before swap:', ethers.utils.formatUnits(reserves._reserve0, 18));

    // Perform a swap from ACoins to WETH
    const amountInACoins = ethers.utils.parseUnits('500', 18); // 500 ACoins
    const amountOutMinWeth = 0; // Accept any amount of WETH

    await aCoins.approve(router.address, amountInACoins).then(tx => tx.wait());
    const swapPathACoinsToWeth = [aCoins.address, weth.address];
    const aCoinsToWethSwapTx = await router.swapExactTokensForTokens(
        amountInACoins,
        amountOutMinWeth,
        swapPathACoinsToWeth,
        deployer.address,
        deadline,
        { gasLimit: ethers.utils.hexlify(1000000) }
    );
    await aCoinsToWethSwapTx.wait();
    console.log('ACoins to WETH swap executed');

    // Fetch and display reserves after the first swap
    reserves = await pair.getReserves();
    console.log('Reserves after ACoins to WETH swap:', reserves);
    console.log('Pair ACoins balance after ACoins to WETH swap:', ethers.utils.formatUnits(reserves._reserve1, 18));
    console.log('Pair WETH balance after ACoins to WETH swap:', ethers.utils.formatUnits(reserves._reserve0, 18));

    // Perform a swap from WETH to ACoins
    const amountInWeth = ethers.utils.parseUnits('0.2', 18); // 0.2 WETH
    const amountOutMinACoins = 0; // Accept any amount of ACoins

    await weth.approve(router.address, amountInWeth).then(tx => tx.wait());
    const swapPathWethToACoins = [weth.address, aCoins.address];
    const wethToACoinsSwapTx = await router.swapExactTokensForTokens(
        amountInWeth,
        amountOutMinACoins,
        swapPathWethToACoins,
        deployer.address,
        deadline,
        { gasLimit: ethers.utils.hexlify(1000000) }
    );
    await wethToACoinsSwapTx.wait();
    console.log('WETH to ACoins swap executed');

    // Fetch and display reserves after the second swap
    reserves = await pair.getReserves();
    console.log('Reserves after WETH to ACoins swap:', reserves);
    console.log('Pair ACoins balance after WETH to ACoins swap:', ethers.utils.formatUnits(reserves._reserve1, 18));
    console.log('Pair WETH balance after WETH to ACoins swap:', ethers.utils.formatUnits(reserves._reserve0, 18));

    // Display deployer's new balance
    const newACoinsBalance = await aCoins.balanceOf(deployer.address);
    const newWethBalance = await weth.balanceOf(deployer.address);
    console.log('New ACoins balance:', ethers.utils.formatUnits(newACoinsBalance, 18));
    console.log('New WETH balance:', ethers.utils.formatUnits(newWethBalance, 18));
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
