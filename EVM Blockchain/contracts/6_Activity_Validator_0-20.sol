// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
interface ILamportBase {

    enum KeyType { MASTER, ORACLE, DELETED }

    function performLamportOracleCheck(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory prepacked
    ) external returns (bool);
    function performLamportMasterCheck(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory prepacked
    ) external returns (bool);

    function getKeyAndIndexByPKH(bytes32 pkh) external view returns (KeyType, bytes32, uint);

}

interface IPlayerDatabase {
    function getOracleKeyIndices(address _address) external view returns (uint256 oracleKeyIndex1, uint256 oracleKeyIndex2);
    function getAllPlayerNames() external view returns (string[] memory);
    function getServerIPList() external view returns (string[] memory);
    function getValidRewardAddressesByNames(string[] memory playerNames) external returns (address[] memory);
    function isValidator(address _address) external view returns (bool);
    function commissionAddress_() external view returns (address);
    function coinCommission_() external view returns (uint256);
}

interface IGP_Mint {
    function mintTokens(address to, uint256 amount) external;
    // Add other function signatures as needed
}
contract GameValidator {

    ILamportBase public lamportBase;

    IPlayerDatabase playerDatabase;
    IGP_Mint public mintContract;
    event MintContractUpdated(address mintContractAddress);
    event PlayerDatabaseAddressUpdated(address playerDatabaseAddress);

    mapping(string => address[]) private validatorsPerServerIP;
    mapping(string => mapping(address => ServerSubmission)) public serverSubmissions; 
    mapping(bytes32 => string[]) public hashToPlayerList; // playerListHash -> playerNames
    mapping(address => address) private proposedMintContractAddresses;
    mapping(address => address) private proposedPlayerDatabaseAddresses;
    mapping(address => bytes32) private submittedPlayerListHashes;

    bytes32 private lastUsedNextPKH;

    uint256 public lastMintTime;
    uint256 public constant MINT_INTERVAL = 5 minutes;
    uint256 public constant MAX_PLAYERS_PER_SUBMISSION = 64;
    uint256 public constant MAX_MINT_TIME = 10 minutes; // 10 minutes cap
    uint256 public constant TOKENS_PER_SECOND = (1e18 * 60) / 60; // 1e18 represents 1 token, and we divide by 60 seconds
    address _playerDatabaseAddress = 0x3b9467De1800bBB6ba6Bd3D1cb7e7BEBC0EFa96f;
    address _mintContractAddress = 0xB05d57719694A1C073707906b0E13efFa5975504;
    constructor(address _lamportBase, address __playerDatabaseAddress, address __mintContractAddress) {
        lamportBase = ILamportBase(_lamportBase);
        playerDatabase = IPlayerDatabase(__playerDatabaseAddress);
        mintContract = IGP_Mint(__mintContractAddress);
    }

    struct ServerSubmission {
        //address validator;
        bytes32 playerListHash; // Hash of the player list for gas efficiency
        bool canMint;
    }

    struct ServerPlayers {
        string serverIP;
        string[] playerNames;
    }
    //mapping(string => ServerSubmission[]) public serverSubmissions; // serverIP -> submissions
    struct HashCount {
        bytes32 hash;
        uint256 count;
    }


    function updateMintContractAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address mintContractAddress
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(mintContractAddress);

        // Perform the Lamport Master Check directly calling lamportBase
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        
        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed for proposed update of Mint contract address");

        // Temporarily store the proposed Mint contract address for the sender
        proposedMintContractAddresses[msg.sender] = mintContractAddress;
        lastUsedNextPKH = nextPKH;
    }

    function updateMintContractAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address mintContractAddress
    ) public {
        // Encode the new contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(mintContractAddress);

        // Perform the Lamport Master Check again

        // Verify that the proposed contract address matches the address being confirmed
        require(proposedMintContractAddresses[msg.sender] == mintContractAddress, "Mint contract address update mismatch");

        // Ensure a different key is used for the confirmation step
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        require(lastUsedNextPKH != currentPKH, "Same PKH used for both steps; use a separate key for confirmation");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed on confirmation of Mint contract address update");

        // Officially update the Mint contract address
        mintContract = IGP_Mint(mintContractAddress);
        emit MintContractUpdated(mintContractAddress);

        // Clear the temporary storage
        delete proposedMintContractAddresses[msg.sender];
        lastUsedNextPKH = bytes32(0);
    }

    // Function to set the PlayerDatabase contract address
    function updatePlayerDatabaseAddressStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address playerDatabaseAddress
    ) public {
        // Encode the new PlayerDatabase contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(playerDatabaseAddress);

        // Perform the Lamport Master Check directly calling lamportBase
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        
        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed for proposed update of PlayerDatabase contract address");

        // Temporarily store the proposed PlayerDatabase contract address for the sender
        proposedPlayerDatabaseAddresses[msg.sender] = playerDatabaseAddress;
        lastUsedNextPKH = nextPKH;
    }

    function updatePlayerDatabaseAddressStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address playerDatabaseAddress
    ) public {
        // Encode the new PlayerDatabase contract address to bytes for the Lamport check
        bytes memory prepacked = abi.encodePacked(playerDatabaseAddress);

        // Perform the Lamport Master Check again

        // Verify that the proposed contract address matches the address being confirmed
        require(proposedPlayerDatabaseAddresses[msg.sender] == playerDatabaseAddress, "PlayerDatabase contract address update mismatch");

        // Ensure a different key is used for the confirmation step
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        require(lastUsedNextPKH != currentPKH, "Same PKH used for both steps; use a separate key for confirmation");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "Authorization failed on confirmation of PlayerDatabase contract address update");

        // Officially update the PlayerDatabase contract address
        playerDatabase = IPlayerDatabase(playerDatabaseAddress);
        emit PlayerDatabaseAddressUpdated(playerDatabaseAddress); // Assuming the existence of this event for traceability

        // Clear the temporary storage
        delete proposedPlayerDatabaseAddresses[msg.sender];
        lastUsedNextPKH = bytes32(0);
    }
    
    function calculateMintAmount() private view returns (uint256) {
        uint256 elapsedSeconds = block.timestamp - lastMintTime;

        if (elapsedSeconds > MAX_MINT_TIME) {
            elapsedSeconds = MAX_MINT_TIME; // Cap the elapsed time to MAX_MINT_TIME
        }

        return elapsedSeconds * TOKENS_PER_SECOND; // Calculate the mint amount based on elapsed time
    }

    function updateValidatorsList(string memory serverIP, address validator) private {
        bool validatorExists = false;
        for (uint i = 0; i < validatorsPerServerIP[serverIP].length; i++) {
            if (validatorsPerServerIP[serverIP][i] == validator) {
                validatorExists = true;
                break;
            }
        }
        if (!validatorExists) {
            validatorsPerServerIP[serverIP].push(validator);
        }
    }

    function submitPlayerListStepOne(
        bytes32 playerListHash,
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH
    ) public {
        // Perform Lamport Oracle check with "1" as the prepacked value


        // Calculate pkh from currentpub to ensure the caller is authorized
        bytes32 pkh = keccak256(abi.encodePacked(currentpub));
        (, , uint index) = lamportBase.getKeyAndIndexByPKH(pkh);
        (uint256 oracleKeyIndex1, uint256 oracleKeyIndex2) = playerDatabase.getOracleKeyIndices(msg.sender);
        require(
            index == oracleKeyIndex1 || index == oracleKeyIndex2,
            "Caller's oracle key index does not match"
        );
        require(
            lamportBase.performLamportOracleCheck(
                currentpub,
                sig,
                nextPKH,
                abi.encodePacked(playerListHash)
            ),
            "Lamport oracle check failed"
        );
        submittedPlayerListHashes[msg.sender] = playerListHash;
    }


    function submitPlayerListStepTwo(ServerPlayers[] memory serverPlayerLists, address validatorID, bool canMintFlag) public {
        require(isValidator(validatorID), "Caller is not a registered validator");
        bytes memory encodedData;
        for (uint i = 0; i < serverPlayerLists.length; i++) {
            encodedData = abi.encodePacked(encodedData, serverPlayerLists[i].serverIP); // Include server IP in the hash
            for (uint j = 0; j < serverPlayerLists[i].playerNames.length; j++) {
                encodedData = abi.encodePacked(encodedData, serverPlayerLists[i].playerNames[j]);
            }
        }
        // bytes32 computedHash = keccak256(encodedData);
        // require(computedHash == submittedPlayerListHashes[validatorID], "List hash does not match previously provided hash.");

        uint256 totalPlayerCount = 0;


        for (uint i = 0; i < serverPlayerLists.length; i++) {
            uint256 serverPlayerCount = serverPlayerLists[i].playerNames.length;
            if (totalPlayerCount + serverPlayerCount > MAX_PLAYERS_PER_SUBMISSION) {
                break; // Stop if the max players per submission is exceeded
            }
            totalPlayerCount += serverPlayerCount;

            // Encode each string in the playerNames array individually
            bytes memory encodedPlayerNames;
            for (uint j = 0; j < serverPlayerLists[i].playerNames.length; j++) {
                encodedPlayerNames = abi.encodePacked(encodedPlayerNames, serverPlayerLists[i].playerNames[j]);
            }

            // Compute the hash of the concatenated byte array
            bytes32 playerListHash = keccak256(encodedPlayerNames);
            hashToPlayerList[playerListHash] = serverPlayerLists[i].playerNames;

            // Update or add the validator to the list for this server IP
            updateValidatorsList(serverPlayerLists[i].serverIP, validatorID);

            // Overwrite the existing submission for this server IP and validator
            serverSubmissions[serverPlayerLists[i].serverIP][validatorID] = ServerSubmission({
                playerListHash: playerListHash,
                canMint: canMintFlag
            });
        }
        // Check if it's time to perform mass minting
        uint256 currentTime = block.timestamp;
        uint256 timeSinceLastMint = currentTime - lastMintTime;
        uint256 timeToNextInterval = MINT_INTERVAL - (currentTime % MINT_INTERVAL);

        if (timeSinceLastMint >= MINT_INTERVAL && timeToNextInterval < MINT_INTERVAL) {
            performMassMinting();
            lastMintTime = currentTime - timeToNextInterval; // Align with the 5-minute interval
        }
    }
    // function submitPlayerList(ServerPlayers[] memory serverPlayerLists, address validatorID, bool canMintFlag) public {
    //     require(isValidator(validatorID), "Caller is not a registered validator");

    //     uint256 totalPlayerCount = 0;

    //     for (uint i = 0; i < serverPlayerLists.length; i++) {
    //         uint256 serverPlayerCount = serverPlayerLists[i].playerNames.length;
    //         if (totalPlayerCount + serverPlayerCount > MAX_PLAYERS_PER_SUBMISSION) {
    //             break; // Stop if the max players per submission is exceeded
    //         }

    //         totalPlayerCount += serverPlayerCount;

    //         // Create a hash for the player list
    //         bytes32 playerListHash = keccak256(abi.encodePacked(serverPlayerLists[i].playerNames));
    //         hashToPlayerList[playerListHash] = serverPlayerLists[i].playerNames;

    //         // Overwrite the existing submission for this server IP and validator
    //         serverSubmissions[serverPlayerLists[i].serverIP][validatorID] = ServerSubmission({
    //             playerListHash: playerListHash,
    //             canMint: canMintFlag
    //         });
    //     }
    // }

    function isValidator(address _address) public view returns (bool) {
        //PlayerDatabase playerDatabase = PlayerDatabase(playerDatabaseAddress);
        return playerDatabase.isValidator(_address);
    }

    function resetSubmissions() private {
        string[] memory serverIPs = playerDatabase.getServerIPList();
        for (uint i = 0; i < serverIPs.length; i++) {
            string memory serverIP = serverIPs[i];
            address[] memory validators = validatorsPerServerIP[serverIP];
            for (uint j = 0; j < validators.length; j++) {
                serverSubmissions[serverIP][validators[j]].canMint = false;
            }
        }
    }

    // Function to perform mass minting
    function performMassMinting() private {
        string[] memory serverIPs = playerDatabase.getServerIPList();
        for (uint i = 0; i < serverIPs.length; i++) {
            string memory serverIP = serverIPs[i];
            bytes32 commonHash = findMostCommonHash(serverIP);
            if (commonHash != bytes32(0)) {
                mintForServer(commonHash);
            }
        }
        resetSubmissions();
    }
    function mintForServer(bytes32 playerListHash) private {
        // Retrieve the player list for the given hash
        //string[] memory playerList = hashToPlayerList[playerListHash];
        string[] memory playerList = new string[](4);
        playerList[0] = "legopowa";
        playerList[1] = "Player1";
        playerList[2] = "Player2";
        playerList[3] = "Player3";
        address[] memory rewardAddresses = getValidRewardAddressesByNames(playerList);

        uint256 playerCount = rewardAddresses.length;
        uint256 mintAmountPerPlayer = calculateMintAmount(); // Define logic for mint amount
        uint256 commissionPercentage = playerDatabase.coinCommission_();

        // Net mint amount per player after subtracting the commission percentage
        uint256 netMintAmountPerPlayer = mintAmountPerPlayer * (10000 - commissionPercentage) / 10000;
        uint256 totalCommission = mintAmountPerPlayer * commissionPercentage / 10000 * playerCount;

        // Mint tokens for each player
        for (uint i = 0; i < rewardAddresses.length; i++) {
            if (rewardAddresses[i] != address(0)) { // Check for valid address
                mintContract.mintTokens(rewardAddresses[i], netMintAmountPerPlayer);
            }
        }

        // Send the total commission to the commission address in one go
        address commissionAddr = playerDatabase.commissionAddress_();
        mintContract.mintTokens(commissionAddr, totalCommission);
    }
    function findMostCommonHash(string memory serverIP) private view returns (bytes32) {
        // Assume validatorsPerServerIP is a mapping that tracks validators per server IP
        address[] memory validators = validatorsPerServerIP[serverIP];
        uint256 majorityThreshold = (validators.length * 60) / 100; // 60% of total validators

        bytes32 majorityHash = bytes32(0);
        uint256 highestCount = 0;

        // Use a structure to keep track of each hash count


        HashCount[] memory hashCounts = new HashCount[](validators.length);

        // Count occurrences of each hash
        for (uint i = 0; i < validators.length; i++) {
            bytes32 currentHash = serverSubmissions[serverIP][validators[i]].playerListHash;
            bool found = false;

            for (uint j = 0; j < hashCounts.length; j++) {
                if (hashCounts[j].hash == currentHash) {
                    hashCounts[j].count++;
                    found = true;
                    break;
                }
            }

            if (!found) {
                hashCounts[i] = HashCount({hash: currentHash, count: 1});
            }

            // Update majority hash if necessary
            if (hashCounts[i].count > highestCount) {
                highestCount = hashCounts[i].count;
                majorityHash = hashCounts[i].hash;
            }
        }

        // Check if the highest count meets the majority threshold
        if (highestCount >= majorityThreshold) {
            return majorityHash;
        }

        return bytes32(0); // No majority found
    }

    // Helper function to check if a hash is present in the tempUniqueHashes array


    function getValidRewardAddressesByNames(string[] memory playerNames) public returns (address[] memory) {
        return playerDatabase.getValidRewardAddressesByNames(playerNames);
    }



    // Additional functions...
}
