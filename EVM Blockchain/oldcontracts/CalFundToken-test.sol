// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "OpenZeppelin/openzeppelin-contracts@5.0.2/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@5.0.2/contracts/access/Ownable.sol";
import "Uniswap/v2-periphery@1.0.0-beta.0/contracts/interfaces/IUniswapV2Router02.sol";
import "Uniswap/v2-core@1.0.1/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
import "Uniswap/v2-core@1.0.1/v2-core/contracts/interfaces/IUniswapV2Pair.sol";

interface IWMATIC {
    function deposit() external payable;
    function withdraw(uint wad) external;
    function transfer(address dst, uint wad) external returns (bool);
}

contract CalFundToken is ERC20, Ownable {
    IUniswapV2Router02 public uniswapRouter;
    IUniswapV2Factory public uniswapFactory;
    IUniswapV2Pair public uniswapPair;
    IWMATIC public wmatic;

    event EthSubsidyProvided(address recipient, uint256 amount);
    event EthSubsidyFailed(address recipient, uint256 amount, uint256 value);
    event SwapFailed(uint256 tokenAmount);
    event SwapSucceeded(uint256 tokenAmount);
    event ApprovalFailed(address spender, uint256 amount);
    event ApprovalSucceeded(address spender, uint256 amount);

    constructor(address initialOwner) ERC20("CalFundToken", "CFT") Ownable(initialOwner) {
        _mint(msg.sender, 1000000 * 10 ** decimals()); // Initial mint for liquidity purposes
    }

    function setUniswapFactory(address _factory) external onlyOwner {
        uniswapFactory = IUniswapV2Factory(_factory);
    }

    function setUniswapRouter(address _router) external onlyOwner {
        uniswapRouter = IUniswapV2Router02(_router);
    }

    function setUniswapPair(address _pair) external onlyOwner {
        uniswapPair = IUniswapV2Pair(_pair);
    }

    function setWmaticAddress(address _wmatic) external onlyOwner {
        wmatic = IWMATIC(_wmatic);
    }

    function createPair() external onlyOwner {
        require(address(uniswapFactory) != address(0), "Uniswap factory not set");
        require(address(this) != address(0), "Token address not set");
        require(address(wmatic) != address(0), "WMATIC address not set");

        address pairAddress = uniswapFactory.createPair(address(this), address(wmatic));
        uniswapPair = IUniswapV2Pair(pairAddress);
    }

    function mint(address recipient, uint256 amount) public onlyOwner {
        (uint256 pureAmount, uint256 ethSubsidy) = extractEthSubsidy(amount);
        _mint(address(this), pureAmount);
        _approve(address(this), address(uniswapRouter), pureAmount);

        if (ethSubsidy > 0) {
            provideEthSubsidy(recipient, ethSubsidy, pureAmount);
        } else {
            _transfer(address(this), recipient, pureAmount);
        }
    }

    function extractEthSubsidy(uint256 amount) internal pure returns (uint256, uint256) {
        uint256 decimals = 18;
        uint256 pureAmount = amount / (10 ** decimals) * (10 ** decimals);
        uint256 ethSubsidy = amount % (10 ** decimals);

        // Check if the subsidy pattern matches .123456000000000000
        if (ethSubsidy / (10 ** 12) == 123456) {
            ethSubsidy = (ethSubsidy % (10 ** 12)) * (10 ** 6); // Only take the last 12 digits and pad six 0s
        } else {
            ethSubsidy = 0; // If not a valid subsidy pattern, set it to 0
        }

        return (pureAmount, ethSubsidy);
    }

    function provideEthSubsidy(address recipient, uint256 ethSubsidy, uint256 pureAmount) internal {
        if (!swapTokensForExactEth(ethSubsidy)) {
            emit EthSubsidyFailed(recipient, ethSubsidy, 1);
            _transfer(address(this), recipient, pureAmount);
            return;
        }

        (bool success,) = recipient.call{value: ethSubsidy}("");
        if (success) {
            emit EthSubsidyProvided(recipient, ethSubsidy);
        } else {
            emit EthSubsidyFailed(recipient, ethSubsidy, 2);
        }

        uint256 adjustedAmount = pureAmount - ethSubsidy;
        _transfer(address(this), recipient, adjustedAmount);
    }

    function swapTokensForExactEth(uint256 ethAmount) private returns (bool) {
        address[] memory path = new address[](2);
        path[0] = address(this);
        path[1] = address(wmatic); // Use wmatic address directly

        uint[] memory amounts = uniswapRouter.getAmountsIn(ethAmount, path);
        uint tokenAmount = amounts[0];

        // Approve the router to spend the tokens from the contract
        try this.approve(address(uniswapRouter), tokenAmount) {
            emit ApprovalSucceeded(address(uniswapRouter), tokenAmount);
        } catch {
            emit ApprovalFailed(address(uniswapRouter), tokenAmount);
            return false;
        }

        try uniswapRouter.swapTokensForExactTokens(
            ethAmount,
            tokenAmount,
            path,
            address(this),
            block.timestamp + 600
        ) {
            emit SwapSucceeded(tokenAmount);
            return true;
        } catch {
            emit SwapFailed(tokenAmount);
            return false;
        }
    }

    function getEthBalance(address addr) public view returns (uint256) {
        return addr.balance;
    }
}
