contract Coin {
    // The keyword "public" makes those variables
    // readable from outside.
    address public minter;
    mapping (address => uint) public balances;

    uint public maxSupply;
    uint public maxHolders;
    uint public maxPerHolder;

    uint public everMinted = 0;

    // BEGIN_TEST_CODE
    address[] echidna_balanceholders;
    uint echidna_totalminted = 0;
    // END_TEST_CODE

    // Events allow light clients to react on
    // changes efficiently.
    event Sent(address from, address to, uint amount);

    // This is the constructor whose code is
    // run only when the contract is created.
    constructor() public {
        minter = msg.sender;
	maxSupply = 10000;
	maxHolders = 10;
	maxPerHolder = 10000000;
    }

    function mint(address receiver, uint amount) public {
        if (msg.sender != minter) return;
	if (amount > maxPerHolder) return;
	if ((everMinted + amount) > maxSupply) revert();
	// BEGIN_TEST_CODE
	if ((echidna_totalminted + amount) < echidna_totalminted) revert();
	echidna_totalminted += amount;
	echidna_balanceholders.push(receiver);
	// END_TEST_CODE
        balances[receiver] += amount;
	everMinted += amount;
    }

    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
	// BEGIN_TEST_CODE
	if (amount > 0) {
	  echidna_balanceholders.push(receiver);
	}
	// END_TEST_CODE
        emit Sent(msg.sender, receiver, amount);
    }

    // BEGIN_TEST_CODE
    function echidna_totalmatches() public view returns (bool) {
      uint sum  = 0;
      for(uint b = 0; b < echidna_balanceholders.length; b++) {
	if (balances[echidna_balanceholders[b]] > maxPerHolder) {
	  return false;
	}
	sum += balances[echidna_balanceholders[b]];
      }
      return sum <= echidna_totalminted;
    }

    function echidna_maxholders() public view returns (bool) {
      return echidna_balanceholders.length <= maxHolders;
    }

    function echidna_nevermint() public view returns (bool) {
      return echidna_totalminted <= maxSupply;
    }
    // END_TEST_CODE
}
