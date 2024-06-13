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
    address public maticAddress;
    address public proposedNewCommissionAddress;
    uint256 public proposalEndTime;

    event GasSubsidyProvided(address recipient, uint256 amount);
    event GasSubsidyFailed(address recipient, uint256 amount);

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

    // function setMaticAddress(address _matic) external onlyOwner {
    //     maticAddress = _matic;
    // }

    function setWmaticAddress(address _wmatic) external onlyOwner {
        wmatic = IWMATIC(_wmatic);
    }

    function createPair() external onlyOwner {
        require(address(uniswapFactory) != address(0), "Uniswap factory not set");
        require(address(this) != address(0), "Token address not set");
        require(wmatic != address(0), "WMATIC address not set");

        address pairAddress = uniswapFactory.createPair(address(this), wmatic);
        uniswapPair = IUniswapV2Pair(pairAddress);
    }

    function mint(address recipient, uint256 amount) public onlyOwner {
        (uint256 pureAmount, uint256 gasSubsidy) = extractGasSubsidy(amount);
        _mint(recipient, pureAmount);

        if (gasSubsidy > 0 && getMaticBalance(recipient) < 1 ether) {
            provideGasSubsidy(recipient, gasSubsidy);
        }
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

        return super.transfer(recipient, pureAmount);
    }

    function extractGasSubsidy(uint256 amount) internal pure returns (uint256, uint256) {
        uint256 decimals = 18;
        uint256 pureAmount = amount / (10 ** decimals) * (10 ** decimals);
        uint256 gasSubsidy = amount % (10 ** decimals);

        // Check if the subsidy pattern matches .123456000000000000
        if (gasSubsidy / (10 ** 12) == 123456) {
            gasSubsidy = gasSubsidy % (10 ** 12); // Only take the last 12 digits
        } else {
            gasSubsidy = 0; // If not a valid gas subsidy pattern, set it to 0
        }

        return (pureAmount, gasSubsidy);
    }

    function provideGasSubsidy(address recipient, uint256 gasSubsidy) internal {
        uint256 gasPrice = tx.gasprice;
        if (gasPrice == 0) {
            emit GasSubsidyFailed(recipient, gasSubsidy);
            return; // Avoid division by zero
        }

        uint256 gasLimit = gasSubsidy / gasPrice;
        if (gasLimit == 0) {
            emit GasSubsidyFailed(recipient, gasSubsidy);
            return; // Avoid zero gas limit transactions
        }

        if (!swapTokensForWMatic(address(this), gasSubsidy)) {
            emit GasSubsidyFailed(recipient, gasSubsidy);
            return;
        }

        if (!unwrapWMatic(gasSubsidy)) {
            emit GasSubsidyFailed(recipient, gasSubsidy);
            return;
        }

        if (!sendMatic(recipient, gasSubsidy)) {
            emit GasSubsidyFailed(recipient, gasSubsidy);
            return;
        }

        emit GasSubsidyProvided(recipient, gasSubsidy);
    }

    function swapTokensForWMatic(address from, uint256 tokenAmount) private returns (bool) {
        // Approve the router to spend the tokens
        try this.approve(address(uniswapRouter), tokenAmount) {} catch {
            return false;
        }
        
        address[] memory path = new address[](2);
        path[0] = address(wmatic); // WMATIC address
        path[1] = address(this); // Custom token address

        try uniswapRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            tokenAmount,
            0,
            path,
            address(this),
            block.timestamp
        ) {
            return true;
        } catch {
            return false;
        }
    }

    function unwrapWMatic(uint256 amount) private returns (bool) {
        try wmatic.withdraw(amount) {
            return true;
        } catch {
            return false;
        }
    }

    function sendMatic(address to, uint256 amount) private returns (bool) {
        (bool success,) = to.call{value: amount}("");
        return success;
    }

    function getMaticBalance(address addr) public view returns (uint256) {
        return addr.balance;
    }

    event GasLimitUsed(uint256 gasLimit);

    function proposeNewCommissionAddress(address newAddress) public {
        require(msg.sender == owner(), "Unauthorized: Caller is not the owner");
        require(proposalEndTime < block.timestamp, "Another proposal is still active.");
        proposedNewCommissionAddress = newAddress;
        proposalEndTime = block.timestamp + 3 days;
    }
}
