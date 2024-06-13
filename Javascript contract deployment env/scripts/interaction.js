require('dotenv').config();
const { ethers } = require('hardhat');
const fs = require('fs');
const path = require('path');

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log('Interacting with contracts using the account:', deployer.address);

    // Load deployed addresses
    const addresses = JSON.parse(fs.readFileSync('deployedAddresses.json'));

    const CalFundToken = await ethers.getContractFactory('CalFundToken');
    const cal = CalFundToken.attach(addresses.cal);

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
    const calBalance = await cal.balanceOf(deployer.address);
    const wethBalance = await weth.balanceOf(deployer.address);
    console.log('Deployer CAL balance:', ethers.utils.formatUnits(calBalance, 18));
    console.log('Deployer WETH balance:', ethers.utils.formatUnits(wethBalance, 18));

    // Add liquidity
    const calAmount = ethers.utils.parseUnits('7500', 18); // 7500 CAL
    const wethAmount = ethers.utils.parseUnits('2', 18); // 2 WETH
    const deadline = Math.floor(Date.now() / 1000) + (10 * 60); // 10 minutes from the current Unix time

    // Approve tokens for liquidity addition
    await cal.approve(router.address, calAmount).then(tx => tx.wait());
    await weth.approve(router.address, wethAmount).then(tx => tx.wait());

    const addLiquidityTx = await router.addLiquidity(
        cal.address,
        weth.address,
        calAmount,
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
    console.log('Pair CAL balance before swap:', ethers.utils.formatUnits(reserves._reserve1, 18));
    console.log('Pair WETH balance before swap:', ethers.utils.formatUnits(reserves._reserve0, 18));

    // Perform a swap from CAL to WETH
    const amountInCal = ethers.utils.parseUnits('500', 18); // 500 CAL
    const amountOutMinWeth = 0; // Accept any amount of WETH

    await cal.approve(router.address, amountInCal).then(tx => tx.wait());
    const swapPathCalToWeth = [cal.address, weth.address];
    const calToWethSwapTx = await router.swapExactTokensForTokens(
        amountInCal,
        amountOutMinWeth,
        swapPathCalToWeth,
        deployer.address,
        deadline,
        { gasLimit: ethers.utils.hexlify(1000000) }
    );
    await calToWethSwapTx.wait();
    console.log('CAL to WETH swap executed');

    // Fetch and display reserves after the first swap
    reserves = await pair.getReserves();
    console.log('Reserves after CAL to WETH swap:', reserves);
    console.log('Pair CAL balance after CAL to WETH swap:', ethers.utils.formatUnits(reserves._reserve1, 18));
    console.log('Pair WETH balance after CAL to WETH swap:', ethers.utils.formatUnits(reserves._reserve0, 18));

    // Perform a swap from WETH to CAL
    const amountInWeth = ethers.utils.parseUnits('0.2', 18); // 0.2 WETH
    const amountOutMinCal = 0; // Accept any amount of CAL

    await weth.approve(router.address, amountInWeth).then(tx => tx.wait());
    const swapPathWethToCal = [weth.address, cal.address];
    const wethToCalSwapTx = await router.swapExactTokensForTokens(
        amountInWeth,
        amountOutMinCal,
        swapPathWethToCal,
        deployer.address,
        deadline,
        { gasLimit: ethers.utils.hexlify(1000000) }
    );
    await wethToCalSwapTx.wait();
    console.log('WETH to CAL swap executed');

    // Fetch and display reserves after the second swap
    reserves = await pair.getReserves();
    console.log('Reserves after WETH to CAL swap:', reserves);
    console.log('Pair CAL balance after WETH to CAL swap:', ethers.utils.formatUnits(reserves._reserve1, 18));
    console.log('Pair WETH balance after WETH to CAL swap:', ethers.utils.formatUnits(reserves._reserve0, 18));

    // Display deployer's new balance
    const newCalBalance = await cal.balanceOf(deployer.address);
    const newWethBalance = await weth.balanceOf(deployer.address);
    console.log('New CAL balance:', ethers.utils.formatUnits(newCalBalance, 18));
    console.log('New WETH balance:', ethers.utils.formatUnits(newWethBalance, 18));
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
