contract test {

        uint _multiplier;

        constructor (uint multiplier) public {
selfdestruct(msg.sender);
        }

        function multiply(uint a) public view returns(uint d)  
        {
             return a * _multiplier;
        }
    }