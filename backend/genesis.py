from flask import Flask
import requests
import logging
from transaction import Transaction
from node import Node
from api import api, global_node
import os
import sys

bootstrap_ip = '0.0.0.0'
bootstrap_port = 5000
port = 5000
node = global_node
# is_bootstrap = os.environ.get('IS_BOOTSTRAP')
is_bootstrap = "1"

ip = '0.0.0.0'

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
        genesis_block = node.create_block(index=0, previous_hash=1, validator=0, capacity=5)
        node.curr_block = genesis_block
        node.wallet.balance += 5043330
        node.curr_block.add_transaction(transaction)
        node.blockchain.add_block(genesis_block)
        print("Wallet balance after adding funds:", node.wallet.balance)
        
        # we are bootstrap
        node.wallet.balance += 10000
        app.run(host=bootstrap_ip, port=bootstrap_port)
        # set the bootstrap id
        node.id = 1
        
    
        app.logger.debug("im boot")
        
    else:
        app.run(host=ip, port=port)
        app.logger.debug("im else")

        json_info = {
            'ip': "0.0.0.0",
            'port': port,
            'pub_key': node.wallet.public_key
        }

        app.logger.debug(json_info)

        url = f'http://:5000/register_node'
        response = requests.post(url, json=json_info)
        response_data = response.json()

        node.id = int(response_data['id'])
    
    

    main()