# LamportVerifierPython

To run, you need these (pip install the ones you need):

brownie, hashlib, decimal, typing, web3, json, typing, eth_utils, lorem, sys, itertools, random, eth_abi, Crypto.Hash, time, struct

You'll also need ganache-cli, which is javascript, but you shouldn't have too much difficulty, it's just a no-fuss local blockchain. 
Install with npm install ganache-cli -g .

To test the script out, type brownie run deploy2, then brownie run LamportTest4.py.

**
Python-usable DEX setup

Calfundtoken-test is a part of the coin pair that can successfully perform swaps.


First in the dir before this type source ./u. Then in this dir, brownie run deploy.py, then interaction.py to make swaps with the coin pair. Make sure there are enough amoy coins in the private key's reserves.

