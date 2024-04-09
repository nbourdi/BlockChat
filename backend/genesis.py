from flask import Flask
import requests
import logging
from transaction import Transaction
from node import Node
from api import api, global_node
import os
import sys

bootstrap_ip = '127.0.0.1'
bootstrap_port = 5000
port = 5000
node = global_node
# is_bootstrap = os.environ.get('IS_BOOTSTRAP')
is_bootstrap = "1"

ip = '127.0.0.1'

app = Flask(__name__)
app.register_blueprint(api)

stake = 5
capacity = 10

# global node
# node = Node(capacity=capacity, stake=stake)

# Configure logging
logging.basicConfig(filename='record.log', level=logging.DEBUG)

def main():
    app.logger.debug("Node ID: %s", node.id)
    app.logger.debug("Node Wallet Public Key: %s", node.wallet.public_key)
    app.logger.debug("Node Blockchain Length: %s", len(node.blockchain.blocks))

if __name__ == "__main__":

    if is_bootstrap == "1":
        
        transaction = Transaction(sender_address='0', receiver_address=node.wallet.public_key, type_of_transaction='coins', amount=5000, nonce=0, message=None)
        genesis_block = node.create_block(index=0, previous_hash=1, validator=0, capacity=node.capacity, current_hash=None)
        #node.curr_block = genesis_block
        node.wallet.balance += 5000
        genesis_block.add_transaction(transaction)
        node.blockchain.add_block(genesis_block)
        #print("Wallet balance after adding funds:", node.wallet.balance)
        node.id = 1
        node.unvalidated_balance = 5000
        # add self to peer ring
        node.add_peer(ip=bootstrap_ip, port="5000", public_key=node.wallet.public_key, balance=node.wallet.balance, id=1)

        app.run(host=bootstrap_ip, port=bootstrap_port)
        # set the bootstrap id

        # for block in node.blockchain.blocks:
        #    # print("ITERATE\n\n")
        #     #print(block.transactions[-1].amount)
        #     print(block.current_hash)
        #     print(block.previous_hash)
        # we are bootstrap
    print("\nBlockchain that ive validated\n")
    for block in node.blockchain.blocks:
        print(block)

    print("\ncurr block\n")
    #print(node.curr_block)
        
    main()
