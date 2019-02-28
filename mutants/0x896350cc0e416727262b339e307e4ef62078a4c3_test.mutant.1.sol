contract test {

        uint _multiplier;

        constructor (uint multiplier) public {
revert();
        }

        function multiply(uint a) public view returns(uint d)  
        {
             return a * _multiplier;
        }
    }