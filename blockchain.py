import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("https://eth-sepolia.g.alchemy.com/v2/-s7ff8rLBkql3G-pCbUdh")
PRIVATE_KEY = os.getenv("840c24f45330092556a6821d7fa9cf3449986bcc4fc73633bd907b144987cc36")
CONTRACT_ADDRESS = os.getenv("0xAAc3dE2e0b9401DeC2f204e3A732B76909AeD629")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

account = w3.eth.account.from_key(PRIVATE_KEY)

with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

def register_hash_on_chain(hash_value):
    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.registerMedia(hash_value).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return w3.to_hex(tx_hash)

def verify_hash_on_chain(hash_value):
    return contract.functions.verifyMedia(hash_value).call()