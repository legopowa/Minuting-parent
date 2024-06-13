import datetime
import os
import sys
from decimal import Decimal

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import HTTPProvider, Web3
from web3.middleware import construct_sign_and_send_raw_middleware, geth_poa_middleware

from eth_defi.chain import install_chain_middleware
from eth_defi.gas import node_default_gas_price_strategy
from eth_defi.revert_reason import fetch_transaction_revert_reason
from eth_defi.token import fetch_erc20_details
from eth_defi.confirmation import wait_transactions_to_complete
from eth_defi.uniswap_v2.deployment import fetch_deployment

# Token addresses (replace these with the actual addresses)
QUOTE_TOKEN_ADDRESS = "0xd9623276393fb5F42981E7Ec241169Dc65674471"  # BUSD
BASE_TOKEN_ADDRESS = "0xce8699120ADDfF75325faB29AAdbA871F880D934"  # Binance custodied ETH on BNB Chain

# Connect to JSON-RPC node
json_rpc_url = "https://rpc-amoy.polygon.technology"



web3 = Web3(HTTPProvider(json_rpc_url))

# Inject PoA middleware for Polygon
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Set gas price strategy
web3.eth.set_gas_price_strategy(node_default_gas_price_strategy)

print(f"Connected to blockchain, chain id is {web3.eth.chain_id}. the latest block is {web3.eth.block_number:,}")

# Uniswap V2 compatible DEX deployment details
dex = fetch_deployment(
    web3,
    factory_address="0xb4eCEDc63A9697270285d628a82835A354c6275a",
    router_address="0x890b88BbCF50514Ef5840eD379D81F59e595fef8",
    init_code_hash="0x779e859e37286996e4cb46370bfef4aabea2d69808163b8419342809124c72a8",
)

print(f"Uniswap v2 compatible router set to {dex.router.address}")

# Read and setup a local private key
private_key = "0x50e0105db0e25befff67c7596b91f72377b0fd8bb6f917ab46b91d7663fceb4c"
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
account: LocalAccount = Account.from_key(private_key)
my_address = account.address

# Enable eth_sendTransaction using this private key
web3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

# Read on-chain ERC-20 token data (name, symbol, etc.)
base = fetch_erc20_details(web3, BASE_TOKEN_ADDRESS)
quote = fetch_erc20_details(web3, QUOTE_TOKEN_ADDRESS)

# Native token balance
gas_balance = web3.eth.get_balance(account.address)

print(f"Your address is {my_address}")
print(f"Your have {base.fetch_balance_of(my_address)} {base.symbol}")
print(f"Your have {quote.fetch_balance_of(my_address)} {quote.symbol}")
print(f"Your have {gas_balance / (10 ** 18)} native token for gas fees")

assert quote.fetch_balance_of(my_address) > 0, f"Cannot add liquidity, as you have zero {quote.symbol} tokens"
assert base.fetch_balance_of(my_address) > 0, f"Cannot add liquidity, as you have zero {base.symbol} tokens"

# Ask for liquidity details
decimal_amount_quote = input(f"How many {quote.symbol} tokens you wish to add as liquidity? ")
decimal_amount_base = input(f"How many {base.symbol} tokens you wish to add as liquidity? ")

# Some input validation
try:
    decimal_amount_quote = Decimal(decimal_amount_quote)
    decimal_amount_base = Decimal(decimal_amount_base)
except ValueError as e:
    raise AssertionError(f"Not a good decimal amount: {e}") from e

# Convert a human-readable number to fixed decimal with 18 decimal places
raw_amount_quote = quote.convert_to_raw(decimal_amount_quote)
raw_amount_base = base.convert_to_raw(decimal_amount_base)

# Approve the router to spend our tokens
approve_quote = quote.contract.functions.approve(dex.router.address, raw_amount_quote)
approve_base = base.contract.functions.approve(dex.router.address, raw_amount_base)

tx_approve_quote = approve_quote.build_transaction(
    {
        "gas": 850_000,
        "from": my_address,
    }
)

tx_approve_base = approve_base.build_transaction(
    {
        "gas": 850_000,
        "from": my_address,
    }
)

# Sign and send the approve transactions
tx_hash_approve_quote = web3.eth.send_transaction(tx_approve_quote)
tx_hash_approve_base = web3.eth.send_transaction(tx_approve_base)

# Wait for approval transactions to be mined
wait_transactions_to_complete(
    web3,
    [tx_hash_approve_quote, tx_hash_approve_base],
    max_timeout=datetime.timedelta(minutes=2),
    confirmation_block_count=1,
)

# Build the add liquidity transaction
add_liquidity = dex.router.functions.addLiquidity(
    QUOTE_TOKEN_ADDRESS,
    BASE_TOKEN_ADDRESS,
    raw_amount_quote,
    raw_amount_base,
    0,  # Min amount of quote tokens to add (set to 0 for simplicity)
    0,  # Min amount of base tokens to add (set to 0 for simplicity)
    my_address,
    int(datetime.datetime.now().timestamp()) + 1000,  # Deadline timestamp
)

tx_add_liquidity = add_liquidity.build_transaction(
    {
        "gas": 1_000_000,
        "from": my_address,
    }
)

# Sign and send the add liquidity transaction
tx_hash_add_liquidity = web3.eth.send_transaction(tx_add_liquidity)

# Wait for the add liquidity transaction to be mined
receipts = wait_transactions_to_complete(
    web3,
    [tx_hash_add_liquidity],
    max_timeout=datetime.timedelta(minutes=2.5),
    confirmation_block_count=1,
)

# Check if the add liquidity transaction succeeded
for completed_tx_hash, receipt in receipts.items():
    if receipt["status"] == 0:
        revert_reason = fetch_transaction_revert_reason(web3, completed_tx_hash)
        raise AssertionError(f"Add liquidity transaction {completed_tx_hash.hex()} failed because of: {revert_reason}")

print("Liquidity added successfully!")
print(f"After adding liquidity, you have {base.fetch_balance_of(my_address)} {base.symbol}")
print(f"After adding liquidity, you have {quote.fetch_balance_of(my_address)} {quote.symbol}")
print(f"After adding liquidity, you have {gas_balance / (10 ** 18)} native token left for gas fees")
