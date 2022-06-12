from solcx import compile_standard,install_solc
import json
from web3 import Web3
import os

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")
compiled_sol = compile_standard(
    {
    "language":"Solidity",
    "sources":{"SimpleStorage.sol": {"content": simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*" : {
                "*" : ["abi","metadata","evm.bytecode","evm.sourceMap"]
            }
        }
    }
    },
    solc_version = "0.6.0", 
)

with open("complied_code.json", "w") as file:
    json.dump(compiled_sol, file)
    
#get bytcode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganaache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x05C62EE42835fE5246eb02498073932c7fd54dd1"
private_key = os.getenv("PRIVATE_KEY")

#create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)
#1. Build Transaction
#2. Sign Transaction
#3. Send Transaction
transaction = SimpleStorage.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chain_id, 
    "from": my_address, 
    "nonce": nonce, 
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#Send txn
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)