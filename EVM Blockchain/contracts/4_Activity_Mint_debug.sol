// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

//import "./LamportBase.sol"; // Adjust the path according to your project structure

// This is a full ERC20 token mint with Lamport permissions on which contract can mint it.
interface ILamportBase {
    function performLamportMasterCheck(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        bytes memory prepacked
    ) external returns (bool);
}

contract Activity_Mint {

    ILamportBase public lamportBase;
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    bytes32 private storedNextPKH;

    uint256 private _totalSupply;

    string private _name;
    string private _symbol;

    // Function to set the authorized minter (Step One)
    address private authorizedMinter;
    mapping(address => address) private proposedMinters; // Temporary storage for proposed minters

    event AuthorizedMinterSet(address indexed minter);
    event AuthorizedMinterRemoved(address indexed minter);

    constructor(
        address lamportBaseAddress,
        address initialAuthorizedMinter,
        string memory __name,
        string memory __symbol
    ) {
        lamportBase = ILamportBase(lamportBaseAddress);
        _name = __name;
        _symbol = __symbol;
        _initializeMintProcess(initialAuthorizedMinter);
    }

    function _initializeMintProcess(address initialAuthorizedMinter) private {
        // Set the authorized minter (it's AnonID contract ok) (hardcoded for one-off execution)
        authorizedMinter = initialAuthorizedMinter;

        // Mint tokens
        _mint(authorizedMinter, 80000 * (10 ** uint256(decimals())));

        // Reset the authorized minter
        authorizedMinter = 0x2BCfFAc2B9EB65C7965008AAB7228e455D81454a;
    }

    function setAuthorizedMinterStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address minter
    ) public {
        // Encode the minter address to bytes
        bytes memory prepacked = abi.encodePacked(minter);

        // Perform the Lamport Master Check
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "LamportBase: Authorization failed");
        storedNextPKH = nextPKH;
        proposedMinters[msg.sender] = minter;
    }
    function viewAuthorizedMinter() public view returns (address) {
        return authorizedMinter;
    }
    function setAuthorizedMinterStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH,
        address minter
    ) public {
        
        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        // Check if storedNextPKH is not the same as the current PKH
        require(currentPKH != storedNextPKH, "LamportBase: Cannot use the same keychain twice for this function");
        
        // Encode the minter address to bytes
        bytes memory prepacked = abi.encodePacked(minter);

        // Perform the Lamport Master Check

        // Check that the proposed minter matches the minter in the current call
        require(proposedMinters[msg.sender] == minter, "MyERC20: Minter address mismatch");

        // Check if the authorized minter is either not set or matches the minter being set
        require(authorizedMinter == address(0) || authorizedMinter == minter, "MyERC20: Another minter already set");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "LamportBase: Authorization failed");

        // Set the authorized minter
        authorizedMinter = minter;

        // Emit the event for setting the authorized minter
        emit AuthorizedMinterSet(minter);

        // Clear the temporary storage for the proposed minter
        delete proposedMinters[msg.sender];
    }

    // testing only
    function debugAddMinter(
        address minter    
    ) public returns (bool) {
        authorizedMinter = minter;
        return true;
    }
    // testing only

    function removeAuthorizedMinterStepOne(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH
    ) public {
        // Encode the authorizedMinter address to bytes
        bytes memory prepacked = abi.encodePacked(authorizedMinter);

        // Perform the Lamport Master Check
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);

        // Ensure that the Lamport Master Check passed
        require(isAuthorized, "LamportBase: Authorization failed");
        storedNextPKH = nextPKH;

        // Set the proposed minter to the zero address
        proposedMinters[msg.sender] = address(0);
    }

    function removeAuthorizedMinterStepTwo(
        bytes32[2][256] calldata currentpub,
        bytes[256] calldata sig,
        bytes32 nextPKH
    ) public {

        bytes32 currentPKH = keccak256(abi.encodePacked(currentpub));
        
        // Check if storedNextPKH is not the same as the current PKH
        require(currentPKH != storedNextPKH, "LamportBase: Cannot use the same keychain twice for this function");
        
        // Encode the authorizedMinter to bytes
        bytes memory prepacked = abi.encodePacked(authorizedMinter);

        // Perform the Lamport Master Check

        // Ensure that the Lamport Master Check passed

        // Check the conditions for removing the minter
        require(proposedMinters[msg.sender] == address(0), "GP_Mint: No minter removal proposed");
        require(authorizedMinter != address(0), "GP_Mint: No minter set");
        bool isAuthorized = lamportBase.performLamportMasterCheck(currentpub, sig, nextPKH, prepacked);
        require(isAuthorized, "LamportBase: Authorization failed");

        // Emit the AuthorizedMinterRemoved event
        emit AuthorizedMinterRemoved(authorizedMinter);

        // Set the authorizedMinter to the zero address
        authorizedMinter = address(0);

        // Clear the temporary storage
        delete proposedMinters[msg.sender];
    }

    // External function to mint tokens, callable by the authorized minter
    function mintTokens(address account, uint256 amount) external {
        require(msg.sender == authorizedMinter, "GP_Mint: Unauthorized minter");
        _mint(account, amount);
    }


    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function decimals() public pure returns (uint8) {
        return 18;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(to != address(0), "ERC20: transfer to the zero address");
        require(_balances[msg.sender] >= value, "ERC20: transfer amount exceeds balance");

        _balances[msg.sender] -= value;
        _balances[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(to != address(0), "ERC20: transfer to the zero address");
        require(value <= _balances[from], "ERC20: transfer amount exceeds balance");
        require(value <= _allowances[from][msg.sender], "ERC20: transfer amount exceeds allowance");

        _balances[from] -= value;
        _balances[to] += value;
        _allowances[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }

    function _mint(address account, uint256 amount) internal {
        require(msg.sender == authorizedMinter, "GP_Mint: Unauthorized minter");
        _totalSupply += amount;
        _balances[account] += amount;
        //emit Minted(address(0), account, amount);
        emit Minted(msg.sender, account, amount);

    }

    function _burn(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: burn from the zero address");
        require(_balances[account] >= amount, "ERC20: burn amount exceeds balance");

        _balances[account] -= amount;
        _totalSupply -= amount;
        emit Transfer(account, address(0), amount);
    }

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Minted(address indexed minter, address indexed account, uint256 amount);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
