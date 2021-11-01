import json
from web3 import Web3
import asyncio
import requests

from contractInfo import contract_address, contract_abi

moralis_mumbai_url = "wss://speedy-nodes-nyc.moralis.io/6249fecc67c24e15fef30131/polygon/mumbai/ws"
web3 = Web3(Web3.WebsocketProvider(moralis_mumbai_url))

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

add_url = "http://192.168.1.211:8000/api/addSubCBBL/"

login_url = "http://192.168.1.211:8000/api/api-token-auth/"
username = "backendLogin"
password = "$$5TiWnAvE"


def handle_deposit(event, token):
    transaction = json.loads(Web3.toJSON(event))
    depositer = (transaction['args']['depositer'])
    amount = (transaction['args']['amount'])/(10**18)
    username = (transaction['args']['username'])
    print(f"Username: {username}, Depositer: {depositer}, Amount: {amount}")
    post_data = {"username": username, "as": "add", "amount": amount}
    headers = {"Authorization": f"Token {token}"}
    req_data = requests.post(url=add_url, data=post_data, headers=headers)
    print(req_data.text)


def handle_withdraw(event, token):
    transaction = json.loads(Web3.toJSON(event))
    withdrawer = (transaction['args']['to'])
    amount = (transaction['args']['amount'])/(10**18)
    username = (transaction['args']['username'])
    print(f"Username: {username}, Withdrawer: {withdrawer}, Amount: {amount}")
    post_data = {"username": username, "as": "sub", "amount": amount}
    headers = {"Authorization": f"Token {token}"}
    req_data = requests.post(url=add_url, data=post_data, headers=headers)
    print(req_data.text)


async def log_loop(transfer_filter, withdraw_filter, poll_interval):
    post_data = {"username": username, "password": password}
    req_data = requests.post(url=login_url, data=post_data)
    token = req_data.json()['token']
    print(token)
    while True:
        for Transfer in transfer_filter.get_new_entries():
            handle_deposit(Transfer, token)
        for Withdraw in withdraw_filter.get_new_entries():
            handle_withdraw(Withdraw, token)
        await asyncio.sleep(poll_interval)


def main():
    transfer_filter = contract.events.Deposit.createFilter(fromBlock='latest')
    withdraw_filter = contract.events.Withdraw.createFilter(fromBlock='latest')
    print("Probably Running...")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(transfer_filter, withdraw_filter, 2)
            )
        )
    finally:
        loop.close()


if __name__ == "__main__":
    main()
