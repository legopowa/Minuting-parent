// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// version 0.09

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol";

interface IWMATIC {
    function deposit() external payable;
    function withdraw(uint wad) external;
    function transfer(address dst, uint wad) external returns (bool);
    function transferFrom(address src, address dst, uint wad) external returns (bool);
    function approve(address guy, uint wad) external returns (bool);
}

contract CalFundToken is ERC20, Ownable {
    IUniswapV2Router02 public uniswapRouter;
    IUniswapV2Factory public uniswapFactory;
    IUniswapV2Pair public uniswapPair;
    IWMATIC public wmatic;
    address public proposedNewCommissionAddress;
    uint256 public proposalEndTime;

    event GasSubsidyProvided(address recipient, uint256 amount);
    event GasSubsidyFailed(address recipient, uint256 amount);
    event GasSubsidyCalculated(uint256 gasPriceWei, uint256 gasSubsidyWei);
    event GasLimitCalculated(uint256 gasLimit);
    event TokensSwappedForWMatic(uint256 tokenAmount);
    event WmaticUnwrapped(uint256 amount);
    event TokensApproved(uint256 amount);
    event TokensSwapped(uint256 amount);
    event MaticSent(address recipient, uint256 amount);

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
    function addLiquidity(uint amountWmatic, uint amountToken, uint amountMinWmatic, uint amountMinToken, uint deadline) external {
        // Transfer WMATIC tokens from msg.sender to the contract
        require(wmatic.transferFrom(msg.sender, address(this), amountWmatic), "Transfer of WMATIC failed");
        // Approve the router to spend WMATIC tokens
        require(wmatic.approve(address(uniswapRouter), amountWmatic), "Approval of WMATIC failed");
        // Transfer Custom tokens from msg.sender to the contract
        require(this.transferFrom(msg.sender, address(this), amountToken), "Transfer of Custom Token failed");
        // Approve the router to spend Custom tokens
        require(this.approve(address(uniswapRouter), amountToken), "Approval of Custom Token failed");

        // Add liquidity
        uniswapRouter.addLiquidity(
            address(wmatic),
            address(this),
            amountWmatic,
            amountToken,
            amountMinWmatic,
            amountMinToken,
            msg.sender,
            deadline
        );
    }
    function createPair() external onlyOwner {
        require(address(uniswapFactory) != address(0), "Uniswap factory not set");
        require(address(this) != address(0), "Token address not set");
        require(address(wmatic) != address(0), "WMATIC address not set");

        address pairAddress = uniswapFactory.createPair(address(this), address(wmatic));
        uniswapPair = IUniswapV2Pair(pairAddress);
    }

    function mint(address recipient, uint256 amount) public onlyOwner {
        (uint256 pureAmount, uint256 gasSubsidy) = extractGasSubsidy(amount);
        _mint(recipient, pureAmount);

        if (gasSubsidy > 0 && getMaticBalance(recipient) < 1 ether) {
            provideGasSubsidy(recipient, gasSubsidy);
        }
        emit GasSubsidyCalculated(tx.gasprice, gasSubsidy);
    }

    function transfer(address recipient, uint256 amount) public override returns (bool) {
        address sender = _msgSender();
        (uint256 pureAmount, uint256 gasSubsidy) = extractGasSubsidy(amount);

        if (gasSubsidy > 0) {
            if (getMaticBalance(sender) < 1 ether && getMaticBalance(recipient) < 1 ether) {
                gasSubsidy *= 2;
                uint256 halfGasSubsidy = gasSubsidy / 2;
                provideGasSubsidy(sender, halfGasSubsidy);
                provideGasSubsidy(recipient, halfGasSubsidy);
            } else if (getMaticBalance(sender) < 1 ether) {
                provideGasSubsidy(sender, gasSubsidy);
            } else if (getMaticBalance(recipient) < 1 ether) {
                provideGasSubsidy(recipient, gasSubsidy);
            }
        }

        bool success = super.transfer(recipient, pureAmount);
        emit GasSubsidyCalculated(tx.gasprice, gasSubsidy);
        return success;
    }

    function extractGasSubsidy(uint256 amount) internal pure returns (uint256, uint256) {
        uint256 decimals = 18;
        uint256 pureAmount = amount / (10 ** decimals) * (10 ** decimals);
        uint256 gasSubsidy = amount % (10 ** decimals);

        uint256 subsidyFactor = (gasSubsidy / (10 ** 15)) % 1000;
        gasSubsidy = subsidyFactor * 10**15; // Convert to MATIC

        return (pureAmount, gasSubsidy);
    }

    function provideGasSubsidy(address recipient, uint256 gasSubsidy) internal {
        // uint256 gasPriceWei = tx.gasprice;
        // if (gasPriceWei == 0) {
        //     emit GasSubsidyFailed(recipient, gasSubsidy);
        //     return; // Avoid division by zero
        // }

        uint256 gasLimit = 500000; // Correct conversion from MATIC to Wei
        emit GasLimitCalculated(gasLimit);
        // if (gasLimit == 0) {
        //     emit GasSubsidyFailed(recipient, gasSubsidy);
        //     return; // Avoid zero gas limit transactions
        // }

        if (!swapTokensForWMatic(address(this), gasSubsidy)) {
            emit GasSubsidyFailed(recipient, 1);
            return;
        }

        if (!unwrapWMatic(gasSubsidy)) {
            emit GasSubsidyFailed(recipient, 2);
            return;
        }

        if (!sendMatic(recipient, gasSubsidy)) {
            emit GasSubsidyFailed(recipient, 3);
            return;
        }

        emit GasSubsidyProvided(recipient, gasSubsidy);
    }

    function swapTokensForWMatic(address from, uint256 tokenAmount) private returns (bool) {
        emit TokensSwappedForWMatic(tokenAmount);

        try this.approve(address(uniswapRouter), tokenAmount) {
            emit TokensApproved(tokenAmount);
        } catch {
            emit GasSubsidyFailed(from, 4); // Emit for approve failure
            return false;
        }

        address[] memory path = new address[](2);
        path[0] = address(this); // Custom token address
        path[1] = address(wmatic); // WMATIC address

        try uniswapRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            tokenAmount,
            0,
            path,
            address(this),
            block.timestamp
        ) {
            emit TokensSwapped(tokenAmount);
            return true;
        } catch {
            emit GasSubsidyFailed(from, 5); // Emit for swap failure
            return false;
        }
    }

    function unwrapWMatic(uint256 amount) private returns (bool) {
        emit WmaticUnwrapped(amount);
        try wmatic.withdraw(amount) {
            return true;
        } catch {
            return false;
        }
    }

    function sendMatic(address to, uint256 amount) private returns (bool) {
        (bool success,) = to.call{value: amount}("");
        emit MaticSent(to, amount);
        return success;
    }

    function getMaticBalance(address addr) public view returns (uint256) {
        return addr.balance;
    }
    
    function getUniswapPair() public view returns (address) {
        return address(uniswapPair);
    }

    function proposeNewCommissionAddress(address newAddress) public {
        require(msg.sender == owner(), "Unauthorized: Caller is not the owner");
        require(proposalEndTime < block.timestamp, "Another proposal is still active.");
        proposedNewCommissionAddress = newAddress;
        proposalEndTime = block.timestamp + 3 days;
    }
}
