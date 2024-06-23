// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// interface IPlayerDatabaseSubcontract {
//     function addOrUpdatePlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered) external;
// }

interface IPlayerDatabase {
    function addOrUpdatePlayer(
        address _address,
        string memory _steamID,
        string memory _playerName,
        uint256 _oracleKeyIndex1,
        uint256 _oracleKeyIndex2,
        address _rewardAddress
    ) external;    
    function deletePlayer(address _address) external;
    // Include other functions from PlayerDatabase that PlayerOnrampContract needs to call

    function setGameAdminStatus(address admin, bool status) external;
    function setValidatorStatus(address validator, bool status) external;

}

contract PlayerOnboardContract {
    IPlayerDatabase public playerDatabase;

    event PlayerOnboarded(address indexed _address, string _steamID, string _playerName, uint256 _oracleKeyIndex1, uint256 _oracleKeyIndex2, address _rewardAddress);
    event PlayerRemoved(address indexed deletedPlayerAddress);
    //address _playerDatabaseAddress = 0x3b9467De1800bBB6ba6Bd3D1cb7e7BEBC0EFa96f;

    constructor(address _playerDatabaseAddress) {
        playerDatabase = IPlayerDatabase(_playerDatabaseAddress);
    }

    // function onboardPlayer(address _address, string calldata _steamID, bool _isValidator, string memory _playerName) public {
    //     // Additional logic and security checks as needed
    //     playerDatabase.addOrUpdatePlayer(_address, _steamID, _isValidator, _playerName);
    //     emit PlayerOnboarded(_address, _steamID, _isValidator, _playerName);
    // }
    function onboardPlayer(
        address _address,
        string memory _steamID,
        string memory _playerName,
        uint256 _oracleKeyIndex1, // Expect this to be provided; revert if 0 for new players
        uint256 _oracleKeyIndex2, // Expect this to be provided; could be 0 if only one key is used
        address _rewardAddress // Reward address for the player
    ) public {
        // Here you might want to include checks for the caller's permissions to onboard a player
        // and other business logic validations.

        // Revert if oracleKeyIndex1 is 0 for new players
        require(_oracleKeyIndex1 != 0, "Oracle key index 1 cannot be zero for new players");

        // Call the PlayerDatabase to add or update the player with new parameters
        playerDatabase.addOrUpdatePlayer(_address, _steamID, _playerName, _oracleKeyIndex1, _oracleKeyIndex2, _rewardAddress);

        // Emit an event with all the provided information
        emit PlayerOnboarded(_address, _steamID, _playerName, _oracleKeyIndex1, _oracleKeyIndex2, _rewardAddress);
    }


    function deletePlayer(address _address) public {
        playerDatabase.deletePlayer(_address);
        emit PlayerRemoved(_address);
    }

    function setPlayerDatabaseAddress(address __playerDatabaseAddress) public {
        playerDatabase = IPlayerDatabase(__playerDatabaseAddress);
    }
    // Additional functions and logic as required for onramping...


    function registerValidator(address validator) public {
        // Add appropriate checks here
        playerDatabase.setValidatorStatus(validator, true);
    }

    function removeValidator(address validator) public {
        // Add appropriate checks here
        playerDatabase.setValidatorStatus(validator, false);
    }

    function registerAdmin(address admin) public {
        // Add appropriate checks here
        playerDatabase.setGameAdminStatus(admin, true);
    }

    function removeAdmin(address admin) public {
        // Add appropriate checks here
        playerDatabase.setGameAdminStatus(admin, false);
    }
}
// contract PlayerOnrampContract {
//     IMintyDatabaseSubcontract public mintyDatabase;

//     event PlayerOnboarded(address indexed playerAddress, string steamID, bool isValidator, bool isRegistered);

//     constructor(address _mintyDatabaseAddress) {
//         mintyDatabase = IMintyDatabaseSubcontract(_mintyDatabaseAddress);
//     }

//     function onboardPlayer(address _address, string calldata _steamID, bool _isValidator, bool _isRegistered) public {
//         // Additional logic and security checks as needed
//         mintyDatabase.addOrUpdatePlayer(_address, _steamID, _isValidator, _isRegistered);
//         emit PlayerOnboarded(_address, _steamID, _isValidator, _isRegistered);
//     }

//     // Additional functions and logic as required for onramping...
// }
