"Differential" mutation analysis evaluation of static analysis for Solidity

The interesting thing to most people will be `comparison.txt`
(comparison of the three analysis tools over solidity by example
contracts + etherscan contracts that compile with solc 0.5.4).  "Soon"
there will be a `comparison424.txt` that extends this to 0.4.24
compiling contracts, but expect that to take some time to generate.

To run the analysis, just:

1.  install universalmutator (`pip install universalmutator`)

2.  install, e.g., slither (`pip install slither-analyzer`)

3.  `python analzyeslither.py >& slither_stats.txt`

Installing Securify is a bit more work, but the analysis works the same and has the same interpretation.
