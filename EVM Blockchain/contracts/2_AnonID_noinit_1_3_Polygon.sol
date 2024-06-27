// SPDX-License-Identifier: MIT
pragma solidity ^0.8.1;

interface ILamportBase {
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

    function getPKHsByPrivilege(uint8 privilege) external view returns (bytes32[] memory);
}
contract AnonIDContract {

    ILamportBase public lamportBase;

    event LogLastCalculatedHash(uint256 hash);

    // free transactional quota section

    struct UserQuota {
        uint256 start; // Index of the oldest timestamp
        uint256 count; // Current count of timestamps
    }

    mapping(address => UserQuota) private userQuotaInfo;
    mapping(address => uint256[500]) private userTxTimestamps; // Example with max 500 transactions
    mapping(address => uint256) public hourlyTxQuota;
    mapping(address => LastPlayedInfo) public lastPlayed;

    event TxRecorded(address indexed _user, uint256 timestamp);
    event QuotaSet(address indexed _address, uint256 _quota);

    // permissions

    mapping(address => bool) public isContractPermitted;
    mapping(address => bool) public whitelist;

    event VerificationFailed(uint256 hashedData);
    event Whitelisted(address indexed _address, bytes32 hashedID);
    event RemovedFromWhitelist(address indexed _address);
    event ContractCreated(address indexed contractAddress);

    bool public lastVerificationResult;

    // profile things

    mapping(address => uint256) public minutesPlayed;
    mapping(address => uint256) public lastClaim;
    mapping(address => uint256) public lastLastClaim;
    mapping(address => bytes32) public addressToHashedID;
    mapping(bytes32 => address) public hashedIDToAddress;
    mapping(bytes32 => uint256) private lastUpdateByHashedID;
    mapping(address => uint256) private lastMinutesUpdateTimestamp;



    event MinutesPlayedIncremented(address indexed user, uint256 _minutes);
    event ClaimedGP(address indexed userAddress, uint256 lastClaimValue, uint256 minutesPlayed);

    struct LastPlayedInfo {
        string gameId;
        uint256 timestamp;
    }


    // globals

    uint256 private lastUsedFreeGasCap;
    address private lastUsedContractAddress;
    address private lastUsedContractAddressForRevoke;
    bytes32 private storedNextPKH;


    uint256 public freeGasCap; // Add this state variable for freeGasFee
    bytes32 public lastUsedBytecodeHash;

    event ContractPermissionGranted(address contractAddress);
    event ContractPermissionRevoked(address contractAddress);
    event FreeGasCapSet(uint256 newFreeGasCap);
 
    // commission section

    event CommissionSet(uint256 newCoinCommission);
    event CommissionAddressSet(address indexed newCommissionAddress);

    uint256 public _coinCommission;
    
    address private _commissionAddress; // ideally make this a quantum-hard contract, commissions go here
    uint256 private lastUsedCommission;
    bytes32 private lastUsedCommissionAddressHash;

    constructor(address __commissionAddress, address lamportBaseAddress, uint256 __coinCommission) {
        _commissionAddress = __commissionAddress;
        lamportBase = ILamportBase(lamportBaseAddress);
        _coinCommission = __coinCommission;
    }


    //AnonID functions
    function setCoinCommissionStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        uint256 newCoinCommission
    )
        public
    {
        // Convert the new commission to bytes and pass it to performLamportMasterCheck
        bytes memory prepacked = abi.encodePacked(newCoinCommission);
        
        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            prepacked
        );
        
        // Require that the Lamport Master check passes
        require(lamportCheckPassed, "Lamport Master validation failed");
        
        // Proceed with updating the commission
        lastUsedCommission = newCoinCommission;
        storedNextPKH = nextPKH;

    }
    function setCoinCommissionStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        uint256 newCoinCommission
    )
        public
    {
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        require(currentPKH != storedNextPKH, "LamportBase: Cannot use the same keychain twice for this function");

        // Convert the new commission to bytes and pass it to performLamportMasterCheck
        bytes memory prepacked = abi.encodePacked(newCoinCommission);
        
        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            prepacked
        );

        // Require that the Lamport Master check passes
        require(lamportCheckPassed, "Lamport Master validation failed");

        // Check the commission range and match with last used commission
        require(newCoinCommission >= 0 && newCoinCommission <= 2000, "Commission should be between 0 and 2000 basis points (0% to 20%)");
        require(newCoinCommission == lastUsedCommission, "Mismatched commission values between steps");

        // Update the coin commission
        _coinCommission = newCoinCommission;

        // Reset the temporary variable
        lastUsedCommission = 0;
        storedNextPKH = bytes32(0);

        emit CommissionSet(newCoinCommission);
    }
    function commissionAddress() public view returns (address) {
        return _commissionAddress;
    }
    function coinCommission() public view returns (uint256) {
        return _coinCommission;
    }

    // Assuming there's a mapping to track the last mint time for each player in each game
    // Mapping for each player's last played information

    function isPlayerActiveInGame(string memory gameID, address player) public view returns (uint8) {
        LastPlayedInfo memory lastPlayedInfo = lastPlayed[player];
        bool isWithinTimeLimit = block.timestamp - lastPlayedInfo.timestamp < 8 minutes;

        // Compare keccak256 hash of strings
        if (isWithinTimeLimit && keccak256(abi.encodePacked(lastPlayedInfo.gameId)) == keccak256(abi.encodePacked(gameID))) {
            return 2; // Player is active in this game and recently minted
        } else if (isWithinTimeLimit && keccak256(abi.encodePacked(lastPlayedInfo.gameId)) != keccak256(abi.encodePacked(gameID))) {
            return 1; // Player is active but in a different game
        }
        return 0; // Player is not currently active
    }

    function addToWhitelist(address _address, string memory anonID) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify whitelist");
        
        bytes32 hashedID = keccak256(abi.encodePacked(anonID));

        // Ensure the address is not already whitelisted
        require(!whitelist[_address], "Address already whitelisted");

        // Ensure the hashedID is not already associated with another address
        require(hashedIDToAddress[hashedID] == address(0) || hashedIDToAddress[hashedID] == _address, "hashedID already in use");

        // Initialize the hourly transaction quota for the address
        hourlyTxQuota[_address] = 5; // Adjust as needed

        // Whitelist the address
        whitelist[_address] = true;

        // Update the address to hashedID mapping and the reverse mapping
        addressToHashedID[_address] = hashedID;
        hashedIDToAddress[hashedID] = _address;

        emit Whitelisted(_address, hashedID);
    }


    function updateAnonID(string memory anonID, address newAddress) external {

        require(isContractPermitted[msg.sender], "Not permitted to modify whitelist");
        require(newAddress != address(0), "New address cannot be zero address");
        bytes32 hashedID = keccak256(abi.encodePacked(anonID));
        
        // Ensure that the hashedID is already registered
        require(hashedIDToAddress[hashedID] != address(0), "hashedID not registered");
        
        // Ensure that only the current address associated with the hashedID can update it
        require(msg.sender == hashedIDToAddress[hashedID], "Only current address can update");
        
        // Check for the day-long timeout
        uint256 lastUpdate = lastUpdateByHashedID[hashedID];
        require(lastUpdate == 0 || block.timestamp - lastUpdate >= 1 days, "Update timeout not yet passed");
        
        // Make sure the new address is not already associated with a different hashedID
        require(addressToHashedID[newAddress] == 0 || addressToHashedID[newAddress] == hashedID, "New address already associated with a different hashedID");

        // Remove the old address from the whitelist
        address oldAddress = hashedIDToAddress[hashedID];
        whitelist[oldAddress] = false;
        delete addressToHashedID[oldAddress];
        
        // Update the whitelist and mappings with the new address
        whitelist[newAddress] = true;
        addressToHashedID[newAddress] = hashedID;
        hashedIDToAddress[hashedID] = newAddress;
        
        // Update the last update time
        lastUpdateByHashedID[hashedID] = block.timestamp;
        
        // Emit events as necessary
        emit RemovedFromWhitelist(oldAddress);
        emit Whitelisted(newAddress, hashedID);
    }



    function toHexString(address _address) internal pure returns (string memory) {
        bytes32 value = bytes32(uint256(uint160(_address)));
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(42);

        str[0] = '0';
        str[1] = 'x';

        for (uint256 i = 0; i < 20; i++) {
            str[2+i*2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3+i*2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }

        return string(str);
    }

    function removeFromWhitelist(address _address) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify whitelist");

        // Ensure the address is indeed whitelisted before removing
        require(whitelist[_address], "Address not found in whitelist");

        // Remove the address from the whitelist
        whitelist[_address] = false;

        // Remove the address and hashedID association from the addressToHashedID mapping
        delete addressToHashedID[_address];
        emit RemovedFromWhitelist(_address);

    }

    function incrementMinutesPlayed(address user, uint256 __minutes) external {
        require(isContractPermitted[msg.sender], "Not permitted to modify minutes played");
        require(__minutes <= 200, "Cannot add more than 200 minutes at a time");

        uint256 currentTime = block.timestamp;
        uint256 lastUpdate = lastMinutesUpdateTimestamp[user];
        // Calculate the time difference in minutes since the last update.
        uint256 timeDifference = (currentTime - lastUpdate) / 60;

        if (__minutes == 200) {
            // For the maximum allowed increment, ensure at least 198 minutes have passed.
            require(timeDifference >= 198, "Insufficient time passed for large increment");
        } else if (__minutes > 5 && __minutes < 200) {
            // For intermediate increments, allow 2 minutes less than the increment itself.
            require(timeDifference >= __minutes - 2, "Insufficient time passed for this increment");
        } else if (__minutes <= 5) {
            // For small increments up to 5 minutes, allow updates every 3 minutes to provide wiggle room.
            //require(timeDifference >= 3, "Update frequency too high for small increment");
            //something needs doing here for production, frequent update mitigation
        }

        // Update the minutes played.
        minutesPlayed[user] += __minutes;
        // Update the last update timestamp to the current time.
        lastMinutesUpdateTimestamp[user] = currentTime;

        emit MinutesPlayedIncremented(user, __minutes);
    }


    function updateLastPlayed(address _address, string memory _gameId) external {
        require(isContractPermitted[msg.sender], "Not permitted to update last played");

        lastPlayed[_address] = LastPlayedInfo({
            gameId: _gameId,
            timestamp: block.timestamp
        });

    }
    // Function to get the minutes played by a user
    function getMinutesPlayed(address user) external view returns (uint256) {
        return minutesPlayed[user];
    }
 // New function to check if an address is whitelisted
    function isWhitelisted(address _address) external view returns (bool) {
        return whitelist[_address];
    }

    function grantActivityContractPermissionStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address contractAddress
    )
        public
    {
        // Convert the contract address to bytes and pass it to performLamportMasterCheck
        bytes memory prepacked = abi.encodePacked(contractAddress);

        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            prepacked
        );

        // Require that the Lamport Master check passes
        require(lamportCheckPassed, "Lamport Master validation failed");

        // Save the contract address for the next step
        lastUsedContractAddress = contractAddress;
        storedNextPKH = nextPKH;
    }
    // Step Two: Apply the permission to the stored contract address
    function grantActivityContractPermissionStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH
    )
        public
    {
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        require(currentPKH != storedNextPKH, "LamportBase: Cannot use the same keychain twice for this function");

        // Convert the last used contract address to bytes and pass it to performLamportMasterCheck
        bytes memory prepacked = abi.encodePacked(lastUsedContractAddress);

        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            prepacked
        );

        // Require that the Lamport Master check passes
        require(lamportCheckPassed, "Lamport Master validation failed");

        // Grant permission to the contract address
        isContractPermitted[lastUsedContractAddress] = true;
        emit ContractPermissionGranted(lastUsedContractAddress);
    }
    // Step One: Store the contract address temporarily
    function revokeActivityContractPermissionStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address contractAddress
    )
        public
    {
        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            abi.encodePacked(contractAddress)
        );

        require(lamportCheckPassed, "Lamport Master validation failed");

        lastUsedContractAddressForRevoke = contractAddress;
        storedNextPKH = nextPKH;
    }

    // Step Two: Revoke the permission for the stored contract address
    function revokeActivityContractPermissionStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH
    )
        public
    {
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        require(currentPKH != storedNextPKH, "LamportBase: Cannot use the same keychain twice for this function");

        
        // Convert the last used contract address for revoking to bytes and pass it to performLamportMasterCheck
        bytes memory prepacked = abi.encodePacked(lastUsedContractAddressForRevoke);

        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            prepacked
        );

        require(lamportCheckPassed, "Lamport Master validation failed");

        isContractPermitted[lastUsedContractAddressForRevoke] = false;
        storedNextPKH = bytes32(0);


        emit ContractPermissionRevoked(lastUsedContractAddressForRevoke);
    }
    

    // Step 1: Temporarily store the hash of the new commission address
    function setCommissionAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address newCommissionAddress
    ) public {
        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            abi.encodePacked(newCommissionAddress)
        );

        require(lamportCheckPassed, "Lamport Master validation failed");

        // Save the hash of the new commission address
        lastUsedCommissionAddressHash = keccak256(abi.encodePacked(newCommissionAddress));
        storedNextPKH = nextPKH;

    }

    // Step 2: Verify and set the commissionAddress
    function setCommissionAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address newCommissionAddress
    ) public {

        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        require(currentPKH != storedNextPKH, "LamportBase: Cannot use the same keychain twice for this function");

        // Convert the new commission address to bytes and pass it to performLamportMasterCheck
        bytes memory prepacked = abi.encodePacked(newCommissionAddress);

        // Perform the Lamport Master check
        bool lamportCheckPassed = lamportBase.performLamportMasterCheck(
            currentpub, 
            sig, 
            nextPKH, 
            prepacked
        );

        require(lamportCheckPassed, "Lamport Master validation failed");

        // Verify the hash of the new commission address matches the saved hash
        require(
            keccak256(prepacked) == lastUsedCommissionAddressHash,
            "Mismatched commission address"
        );

        // Update the commission address
        _commissionAddress = newCommissionAddress;
        storedNextPKH = bytes32(0);

        // Emit an event if needed
        // emit CommissionAddressSet(newCommissionAddress);
    }



}
