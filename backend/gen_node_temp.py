from flask import Flask
import requests
import logging
from node import Node
from api import api 
import os
import sys

bootstrap_ip = '0.0.0.0'
bootstrap_port = 5000
port = 5000

# is_bootstrap = os.environ.get('IS_BOOTSTRAP')
is_bootstrap = "1"

ip = '0.0.0.0'

app = Flask(__name__)
app.register_blueprint(api)

stake = 5
capacity = 10

node = Node(capacity=capacity, stake=stake)

# Configure logging
logging.basicConfig(filename='record.log', level=logging.DEBUG)

def main():
    app.logger.debug("Node ID: %s", node.id)
    app.logger.debug("Node Wallet Public Key: %s", node.wallet.public_key)
    app.logger.debug("Node Blockchain Length: %s", len(node.blockchain.blocks))

if __name__ == "__main__":

    
    app.run(host="127.0.0.1", port=5001)
    app.logger.debug("im node1 test temp")

    json_info = {
        'ip': "127.0.0.1",
        'port': 5001,
        'pub_key': node.wallet.public_key
    }

    url = f'http://127.0.0.1:5000/register_node' # NOT FOR DOCKER ONLY PROCESSES
    response = requests.post(url, json=json_info)
    response_data = response.json()

    node.id = int(response_data['id'])

    main()