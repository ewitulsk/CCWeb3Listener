from web3 import Web3
from contractInfo import contract_abi, contract_address


def reqIncrease(addr, amount):
    print("starting reqIncrease")
    private_key = "182bd84b29e5f1533d17d4eacd5637aa15cc560244c3c7ee5743b60888c6ca98"
    moralis_mumbai_url = "wss://speedy-nodes-nyc.moralis.io/6249fecc67c24e15fef30131/polygon/mumbai/ws"
    web3 = Web3(Web3.WebsocketProvider(moralis_mumbai_url))

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    allowed = contract.functions.getAllowed(addr).call()

    print(allowed)

    transaction = contract.functions.increaseAllowed(addr, amount).buildTransaction()

    signed = web3.eth.account.sign_transaction(transaction, private_key)

    ret = web3.eth.send_raw_transaction(signed.rawTransaction)

    print(ret)


def main():
    reqIncrease("0x16d999E396e8623b62D65084557c3DD17D59404F", 100)


if __name__ == "__main__":
    print("Running main")
    main()