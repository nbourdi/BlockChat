from flask import Flask
import requests
from node import Node
from api import app
from transaction import Transaction


bootstrap_ip = '127.0.0.1'
bootstrap_port = 5000
port = 5000

import os

is_bootstrap = os.environ.get('IS_BOOTSTRAP')

ip = '127.0.0.1'

appp = Flask(__name__)
appp.register_blueprint(app)

stake = 5
capacity = 10

node = Node(capacity=capacity, stake=stake)

def main():
    print("Node ID:", node.id)
    print("Node Wallet Public Key:", node.wallet.public_key)
    print("Node Blockchain Length:", len(node.blockchain.blocks))

if __name__ == "__main__":

    if is_bootstrap == 1:
        # we are bootstrap
        node.id=0
        genesis_block = node.create_block(index=0, previous_hash=1, validator=0, capacity=5)
        node.blockchain.blocks.append(genesis_block)


        print("Genesis Block Index:", genesis_block.index)
        print("Genesis Block Previous Hash:", genesis_block.previous_hash)
        print("Genesis Block Validator:", genesis_block.validator)
        print("Genesis Block Capacity:", genesis_block.capacity) 
        print("new Node Blockchain Length:", len(node.blockchain.blocks))


        transaction = Transaction(sender_address='0', receiver_address=f'{node.wallet.public_key}', type_of_transaction='coins', amount=5000, noance=0, message=None)
        genesis_block.add_transaction(transaction)
        print("Genesis Block transactions:", genesis_block.transactions)
        for transaction in genesis_block.transactions:
            print("Transaction ID:", transaction.transaction_id)
            print("Sender Address:", transaction.sender_address)
            print("Receiver Address:", transaction.receiver_address)
            print("Type of Transaction:", transaction.type_of_transaction)
            print("Amount:", transaction.amount)
            print("Nonce:", transaction.nonce)
            print("Message:", transaction.message)
            print()

        appp.run(bootstrap_ip, bootstrap_port)
        # set the bootstrap id
    
    else:
        appp.run(ip, port)

        json_info = {
            'ip': "127.0.0.1",
            'port': port,
            'pub_key': node.wallet.public_key
        }
        print(json_info)

        url = f'http://{bootstrap_ip}:{bootstrap_port}/register_node'
        response = requests.post(url, json=json_info)
        response_data = response.json()

        node.id = int(response_data['id'])

    main()
