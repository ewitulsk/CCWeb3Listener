import json
from web3 import Web3
import asyncio

from contractInfo import contract_address, contract_abi

private_key = "182bd84b29e5f1533d17d4eacd5637aa15cc560244c3c7ee5743b60888c6ca98"

recipient_addr = "0xF20A11663C447B42A5551995554Dab3d249FD721"
amount = 20

moralis_mumbai_url = "wss://speedy-nodes-nyc.moralis.io/6249fecc67c24e15fef30131/polygon/mumbai/ws"
web3 = Web3(Web3.WebsocketProvider(moralis_mumbai_url))

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

withdraw_txn = contract.functions.withdraw(recipient_addr, amount)

signed_txn = web3.eth.account.sign_transaction(withdraw_txn, private_key=private_key)
print(signed_txn.hash)

web3.eth.send_raw_transaction(signed_txn.rawTransaction)


