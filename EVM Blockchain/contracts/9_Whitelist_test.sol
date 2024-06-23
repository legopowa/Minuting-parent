// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAnonIDContract {
    function addToWhitelist(address _address, string calldata anonID) external;
    function removeFromWhitelist(address _address) external;
    function incrementMinutesPlayed(address user, uint256 _minutes) external;
}

contract Whitelist {
    IAnonIDContract anonIDContract;

    event OperationResult(bool success, string message);
    event ErrorCaught(string action, string error);

    constructor(address _systemContractAddress) {
        anonIDContract = IAnonIDContract(_systemContractAddress);
    }

    function addAddressToWhitelist(address _address, string memory anonID) public {
        try anonIDContract.addToWhitelist(_address, anonID) {
            emit OperationResult(true, "Address successfully whitelisted");
        } catch Error(string memory reason) {
            emit OperationResult(false, reason);
            emit ErrorCaught("addAddressToWhitelist", reason);
        } catch {
            emit OperationResult(false, "addToWhitelist failed without a specific revert reason");
            emit ErrorCaught("addAddressToWhitelist", "Unknown failure");
        }
    }

    function removeAddressFromWhitelist(address _address) public {
        try anonIDContract.removeFromWhitelist(_address) {
            emit OperationResult(true, "Address successfully removed from whitelist");
        } catch Error(string memory reason) {
            emit OperationResult(false, reason);
            emit ErrorCaught("removeFromWhitelist", reason);
        } catch {
            emit OperationResult(false, "removeFromWhitelist failed without a specific revert reason");
            emit ErrorCaught("removeFromWhitelist", "Unknown failure");
        }
    }

    function addMinutesPlayed(address user, uint256 _minutes) public {
        try anonIDContract.incrementMinutesPlayed(user, _minutes) {
            emit OperationResult(true, "Minutes played added successfully");
        } catch Error(string memory reason) {
            emit OperationResult(false, reason);
            emit ErrorCaught("addMinutesPlayed", reason);
        } catch {
            emit OperationResult(false, "incrementMinutesPlayed failed without a specific revert reason");
            emit ErrorCaught("addMinutesPlayed", "Unknown failure");
        }
    }
}
