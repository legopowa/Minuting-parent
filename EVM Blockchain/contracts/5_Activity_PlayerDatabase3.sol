// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ILamportBase {

    enum KeyType { MASTER, ORACLE, DELETED }

    function performLamportMasterCheck(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory prepacked
    ) external returns (bool);
    
    function performLamportOracleCheck(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory prepacked
    ) external returns (bool);

    function getKeyAndIndexByPKH(bytes32 pkh) external view returns (KeyType, bytes32, uint);
}

interface IAnonID {
    function incrementMinutesPlayed(address user, uint256 _minutes) external;
    function updateLastPlayed(address _address, string memory _gameId) external;
    function isWhitelisted(address _address) external view returns (bool);
    function isPlayerActiveInGame(string memory gameID, address player) external view returns (uint8);
    function commissionAddress() external view returns (address);
    function coinCommission() external view returns (uint256);
}

contract PlayerDatabase  {
    mapping(string => bool) public gameServerIPs; // Mapping to store game server IPs
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => address) private proposedAnonIDContractAddresses;
    mapping(address => address) private proposedGameValContractAddresses;
    mapping(address => address) private proposedOnrampContractAddresses;
    mapping(address => address) private proposedForumContractAddresses;

    string gameID = "TFC"; // Define your game ID for TFC
    string[] public serverIPList; // Array for listing all server IPs

    // Player Database variables
    struct Player {
        bool isRegistered;
        bool isValidator;
        bool isModerator;
        bool isTourneyMod;
        bool isGameAdmin;
        bool isOnboardQueuer;
        bool isOnboardRegistrar;
        string playerName; // Name of the player
        bytes32 forumKey; // Unique key for forum entitlements
        string steamID;
        address rewardAddress;
        uint256 oracleKeyIndex1;
        uint256 oracleKeyIndex2;
        uint256 lastMintTime; // Adding lastMintTime to the Player struct
    }

    mapping(address => Player) public playerData;
    address[] public playerAddresses;

    // Shared variables
    address public gameValContract; // Address of the game subcontractor
    IAnonID public anonIDContract; // Reference to the AnonID contract
    address public onrampContract; // Address of the onramp contract
    address public forumContract; // Address of the forum contract
    ILamportBase public lamportBase; // Reference to the lamportBase contract
    bytes32 private lastUsedNextPKH;

    // Events
    event ForumContractUpdated(address indexed newForumContract);
    event AnonIDContractUpdated(address indexed newAnonIDContract);
    event GameValContractUpdated(address indexed newGameValContract);
    event OnrampContractUpdated(address indexed newOnrampContract);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event OracleKeyIndicesRetrieved(
        address indexed player,
        uint256 oracleKeyIndex1,
        uint256 oracleKeyIndex2,
        uint256 retrievedIndex
    );

    event Error(
        string errorType,
        address indexed player,
        uint256 retrievedIndex,
        uint256 oracleKeyIndex1,
        uint256 oracleKeyIndex2
    );

    event GameServerIPUpdated(
        string serverIP,
        bool added
        //address indexed player
    );

    event EncodedServerIP(
        string serverIP,
        bytes encodedServerIP
    );
    event OperationResult(bool success, string message);

    // Constructor
    constructor(address _lamportBase, address _anonID) {
        lamportBase = ILamportBase(_lamportBase);
        anonIDContract = IAnonID(_anonID);
        serverIPList.push("172.93.101.194:27015");
        serverIPList.push("63.143.56.124:27015");
        serverIPList.push("64.31.28.179:27015");
        serverIPList.push("172.233.224.83:27015");
    }
    
    function isValidator(address _address) public view returns (bool) {
        return playerData[_address].isValidator;
    }
    function isModerator(address _address) public view returns (bool) {
        return playerData[_address].isModerator;
    }

    function isRegistered(address _address) public view returns (bool) {
        return playerData[_address].isRegistered;
    }
    
    function isTourneyMod(address _address) public view returns (bool) {
        return playerData[_address].isTourneyMod;
    }
    
    function isGameAdmin(address _address) public view returns (bool) {
        return playerData[_address].isGameAdmin;
    }
    
    function isOnboardQueuer(address _address) public view returns (bool) {
        return playerData[_address].isOnboardQueuer;
    }
    
    function isOnboardRegistrar(address _address) public view returns (bool) {
        return playerData[_address].isOnboardRegistrar;
    }

    function commissionAddress_() external view returns (address) {
        return anonIDContract.commissionAddress();
    }

    function coinCommission_() external view returns (uint256) {
        return anonIDContract.coinCommission();
    }
    
    function getOracleKeyIndices(address _address) public view returns (uint256, uint256) {
        require(isRegistered(_address), "Player is not registered");
        return (playerData[_address].oracleKeyIndex1, playerData[_address].oracleKeyIndex2);
    }

    function getValidRewardAddressesByNames(string[] memory playerNames) external returns (address[] memory) {
        require(msg.sender == gameValContract, "Only the game validator contract can access this list");

        address[] memory validRewardAddresses = new address[](playerNames.length);

        for (uint i = 0; i < playerNames.length; i++) {
            for (uint j = 0; j < playerAddresses.length; j++) {
                if (keccak256(abi.encodePacked(playerData[playerAddresses[j]].playerName)) == keccak256(abi.encodePacked(playerNames[i]))) {
                    uint8 playerStatus = anonIDContract.isPlayerActiveInGame(gameID, playerAddresses[j]);

                    if (playerStatus == 2) { // Player already minted for TFC
                        validRewardAddresses[i] = playerData[playerAddresses[j]].rewardAddress;
                        // Increment the minutes played using block.timestamp
                        uint256 minutesPlayed = (block.timestamp - playerData[playerAddresses[j]].lastMintTime) / 60; // Convert seconds to minutes
                        anonIDContract.incrementMinutesPlayed(playerAddresses[j], minutesPlayed);
                        anonIDContract.updateLastPlayed(playerAddresses[j], gameID);
                        playerData[playerAddresses[j]].lastMintTime = block.timestamp; // Update the lastMintTime after minting

                    } else if (playerStatus == 0) { // Player not in a game, flag as active
                        anonIDContract.updateLastPlayed(playerAddresses[j], gameID);
                        // Do not include this player in the reward addresses for this round
                    }
                    break; // Stop the inner loop once the player is processed
                }
            }
        }

        return validRewardAddresses;
    }

    function updateGameServerIP(
        string memory serverIP,
        bool add,
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH
    ) public {
        // Calculate pkh from currentpub
        bytes32 pkh = keccak256(abi.encodePacked(currentpub));

        // Perform Lamport Oracle check with "1" as the prepacked value
        (bool oracleCheckPassed) = lamportBase.performLamportMasterCheck(
            currentpub,
            sig,
            nextPKH,
            abi.encodePacked(serverIP)
        );

        if (!oracleCheckPassed) {
            emit OperationResult(false, "Failed oracle check");
            // Do not exit, just log and continue
        }

        // Retrieve oracle key index and type by PKH
        (, , uint index) = lamportBase.getKeyAndIndexByPKH(pkh);

        // Retrieve player's oracle key indices
        (uint256 oracleKeyIndex1, uint256 oracleKeyIndex2) = getOracleKeyIndices(msg.sender);

        // Emit the oracle key indices before the first require statement
        emit OracleKeyIndicesRetrieved(msg.sender, oracleKeyIndex1, oracleKeyIndex2, index);

        // Ensure the current index matches one of the player's oracle key indices
        if (index != oracleKeyIndex1 && index != oracleKeyIndex2) {
            emit OperationResult(false, "Caller's oracle key index does not match");
            // Do not exit, just log and continue
        }

        // Proceed with the original logic after passing the oracle check and index match
        if (!playerData[msg.sender].isGameAdmin) {
            emit OperationResult(false, "Caller is not a game admin");
            // Do not exit, just log and continue
        }

        bytes memory encodedServerIP = abi.encodePacked(serverIP);
        emit EncodedServerIP(serverIP, encodedServerIP);

        if (add) {
            if (!gameServerIPs[serverIP]) {
                gameServerIPs[serverIP] = true;
                serverIPList.push(serverIP);
                emit GameServerIPUpdated(serverIP, true);
            }
        } else {
            if (gameServerIPs[serverIP]) {
                gameServerIPs[serverIP] = false;
                removeServerIPFromArray(serverIP);
                emit GameServerIPUpdated(serverIP, false);
            }
        }

        emit OperationResult(true, "Operation completed with logging");
    }

    // Helper function to remove a server IP from the array
    function removeServerIPFromArray(string memory serverIP) private {
        require(playerData[msg.sender].isGameAdmin, "Caller is not a game admin");
        for (uint i = 0; i < serverIPList.length; i++) {
            if (keccak256(abi.encodePacked(serverIPList[i])) == keccak256(abi.encodePacked(serverIP))) {
                // Update the mapping to reflect the server IP is no longer registered
                gameServerIPs[serverIP] = false;

                // Remove the server IP from the array
                serverIPList[i] = serverIPList[serverIPList.length - 1];
                serverIPList.pop();
                break;
            }
        }
    }

    // Function to get the full list of server IPs
    function getServerIPList() external view returns (string[] memory) {
        return serverIPList;
    }

    function addOrUpdatePlayer(
        address _address,
        string memory _steamID,
        string memory _playerName,
        uint256 _oracleKeyIndex1, // Revert for new players if this is 0
        uint256 _oracleKeyIndex2,
        address _rewardAddress
    ) 
        public 
    {
        require(msg.sender == onrampContract, "Only the onramp contract can add/update players");
        require(anonIDContract.isWhitelisted(_address), "Address not whitelisted in AnonID");

        Player storage player = playerData[_address];
        if (player.isRegistered) {
            // Update existing player data
            player.steamID = _steamID;
            player.playerName = _playerName;
            if (_rewardAddress != address(0)) {
                player.rewardAddress = _rewardAddress;
            }
            else player.rewardAddress = _address;
            // If _oracleKeyIndex is not 0, update the oracleKeyIndex. Otherwise, leave it unchanged.
            if (_oracleKeyIndex1 != 0) {
                player.oracleKeyIndex1 = _oracleKeyIndex1;
            }
            if (_oracleKeyIndex2 != 0) {
                player.oracleKeyIndex2 = _oracleKeyIndex2;
            }
            // No additional action required for existing players with _oracleKeyIndex = 0
        } else {
            // For a new player, revert the transaction if _oracleKeyIndex is 0
            require(_oracleKeyIndex1 != 0 || _oracleKeyIndex2 != 0, "Oracle key index cannot be zero for new players");

            // Since we're here, _oracleKeyIndex is guaranteed not to be 0
            playerData[_address] = Player({
                steamID: _steamID,
                isValidator: false,
                isRegistered: true,
                rewardAddress: _address,
                playerName: _playerName,
                isModerator: false,
                isTourneyMod: false,
                isGameAdmin: false,
                isOnboardQueuer: false,
                isOnboardRegistrar: false,
                forumKey: 0,
                oracleKeyIndex1: _oracleKeyIndex1, // Directly set the provided index
                oracleKeyIndex2: _oracleKeyIndex2,
                lastMintTime: block.timestamp // Initialize lastMintTime to the current timestamp for new players
            });
            playerAddresses.push(_address);
        }
    }

    function deletePlayer(address _address) public {
        require(msg.sender == onrampContract, "Only the onramp contract can delete players");

        delete playerData[_address]; // Remove player data from mapping

        // Find and remove address from playerAddresses array
        for (uint i = 0; i < playerAddresses.length; i++) {
            if (playerAddresses[i] == _address) {
                playerAddresses[i] = playerAddresses[playerAddresses.length - 1]; // Swap with the last element
                playerAddresses.pop(); // Remove the last element
                break;
            }
        }
    }

    function getAllPlayerNames() public view returns (string[] memory) {
        string[] memory playerNames = new string[](playerAddresses.length);

        for (uint i = 0; i < playerAddresses.length; i++) {
            Player storage player = playerData[playerAddresses[i]];
            playerNames[i] = player.playerName;
        }

        return playerNames;
    }

    function updateAnonIDContractAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _anonIDContract
    ) public {
        // Encode the new contract address to bytes
        bytes memory prepacked = abi.encodePacked(_anonIDContract);

        // Directly call performLamportMasterCheck
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        
        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "LamportBase: Authorization failed");

        // Save the proposed AnonID contract address in a global variable
        proposedAnonIDContractAddresses[msg.sender] = _anonIDContract;
        lastUsedNextPKH = nextPKH;
    }

    function updateAnonIDContractAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _anonIDContract
    ) public {
        // Encode the new contract address to bytes
        bytes memory prepacked = abi.encodePacked(_anonIDContract);

        // Check that the proposed contract address matches the address in the current call
        require(proposedAnonIDContractAddresses[msg.sender] == _anonIDContract, "Proposed AnonID contract address mismatch");

        // Check if the used NextPKH matches the last used PKH to prevent replay with the same keys
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        require(lastUsedNextPKH != currentPKH, "LamportBase: PKH matches last used PKH (use separate second key)");
        // Perform the Lamport Master Check again
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "LamportBase: Authorization failed");
        
        // Update the AnonID contract address
        anonIDContract = IAnonID(_anonIDContract);
        emit AnonIDContractUpdated(_anonIDContract);

        // Clear the temporary storage
        delete proposedAnonIDContractAddresses[msg.sender];
        lastUsedNextPKH = bytes32(0);
    }

    function updateGameValContractAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _gameValContract
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(_gameValContract);

        // Directly call performLamportMasterCheck from lamportBase
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        
        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed for proposed GameVal contract address");

        // Store the proposed GameVal contract address for the sender
        proposedGameValContractAddresses[msg.sender] = _gameValContract;
        lastUsedNextPKH = nextPKH;
    }

    function updateGameValContractAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _gameValContract
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(_gameValContract);

        // Perform the Lamport Master Check again

        // Check that the proposed contract address matches the address being confirmed
        require(proposedGameValContractAddresses[msg.sender] == _gameValContract, "Proposed GameVal contract address mismatch");

        // Check if the used NextPKH matches the last used PKH to ensure a different key is used
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        require(lastUsedNextPKH != currentPKH, "Same PKH used for both steps; use a separate key for confirmation");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed on confirmation of GameVal contract address");

        // Update the GameVal contract address
        gameValContract = _gameValContract;
        emit GameValContractUpdated(_gameValContract);

        // Clear the temporary storage
        delete proposedGameValContractAddresses[msg.sender];
        lastUsedNextPKH = bytes32(0);
    }

    function updateOnrampContractAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _onrampContract
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(_onrampContract);

        // Perform the Lamport Master Check directly calling lamportBase
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        
        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed for updating Onramp contract address");

        // Temporarily store the proposed Onramp contract address for the sender
        proposedOnrampContractAddresses[msg.sender] = _onrampContract;
        lastUsedNextPKH = nextPKH;
    }

    function updateOnrampContractAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _onrampContract
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(_onrampContract);

        // Perform the Lamport Master Check again

        // Verify that the proposed contract address matches the address being confirmed
        require(proposedOnrampContractAddresses[msg.sender] == _onrampContract, "Onramp contract address update mismatch");

        // Ensure a different key is used for the confirmation step
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        require(lastUsedNextPKH != currentPKH, "Same PKH used for both steps; use a separate key for confirmation");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed on confirmation of Onramp contract address update");

        // Officially update the Onramp contract address
        onrampContract = _onrampContract;
        emit OnrampContractUpdated(_onrampContract);

        // Clear the temporary storage
        delete proposedOnrampContractAddresses[msg.sender];
        lastUsedNextPKH = bytes32(0);
    }

    function updateForumContractAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _forumContract
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(_forumContract);

        // Perform the Lamport Master Check directly calling lamportBase
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        
        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed for proposed update of Forum contract address");

        // Temporarily store the proposed Forum contract address for the sender
        proposedForumContractAddresses[msg.sender] = _forumContract;
        lastUsedNextPKH = nextPKH;
    }

    function updateForumContractAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address _forumContract
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(_forumContract);

        // Perform the Lamport Master Check again

        // Verify that the proposed contract address matches the address being confirmed
        require(proposedForumContractAddresses[msg.sender] == _forumContract, "Forum contract address update mismatch");

        // Ensure a different key is used for the confirmation step
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        require(lastUsedNextPKH != currentPKH, "Same PKH used for both steps; use a separate key for confirmation");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed on confirmation of Forum contract address update");

        // Officially update the Forum contract address
        forumContract = _forumContract;
        emit ForumContractUpdated(_forumContract);

        // Clear the temporary storage
        delete proposedForumContractAddresses[msg.sender];
        lastUsedNextPKH = bytes32(0);
    }

    function setModeratorStatus(address _player, bool _status) external {
        require(msg.sender == forumContract, "Only the forum contract can modify moderator status");
        playerData[_player].isModerator = _status;
    }

    function setTourneyModStatus(address _player, bool _status) external {
        require(msg.sender == forumContract, "Only the forum contract can modify tournament moderator status");
        playerData[_player].isTourneyMod = _status;
    }

    function setForumKey(address _player, bytes32 _key) external {
        require(msg.sender == forumContract, "Only the forum contract can set forum key");
        playerData[_player].forumKey = _key;
    }

    function setGameAdminStatus(address admin, bool status) external {
        require(msg.sender == onrampContract, "Only the onramp contract can change Admin status");
        playerData[admin].isGameAdmin = status;
    }

    function setValidatorStatus(address validator, bool status) external {
        require(msg.sender == onrampContract, "Only the onramp contract can change Game Validator status");
        playerData[validator].isValidator = status;
    }
    
    function setOnboardQueuerStatus(address oracle, bool status) external {
        require(msg.sender == onrampContract, "Only the onramp contract can change Onboard Queuer status");
        playerData[oracle].isOnboardQueuer = status;
    }
    
    function setOnboardRegistrarStatus(address oracle, bool status) external {
        require(msg.sender == onrampContract, "Only the onramp contract can change Onboard Registrar Status");
        playerData[oracle].isOnboardRegistrar = status;
    }
}
