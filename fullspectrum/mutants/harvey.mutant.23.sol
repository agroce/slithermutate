pragma solidity ^0.5.4;

contract Foo {
  bool state = true;
  bool saw42 = false;
  function f(int256 a, int256 b, int256 c) public returns (int256) {
    int256 d = b + c;
    if (a == 42) {
       saw42 = true;
    }
    if (d == 1) {
      if (b < 3) {
        return 1;
      }
      if (a == 42) {
        state = false;
        return 2;
      }
      return 3;
    } else {
      if (c < 42) {
        return 4;
      }
      return 5;
    }
  }

  function echidna_state() public view returns (bool) { return(state || saw42); }
}
