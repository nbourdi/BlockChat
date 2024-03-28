from flask import Flask
import requests
from node import Node
from api import app 

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
        appp.run(bootstrap_ip, bootstrap_port)
        # set the bootstrap id
        node.id = 1
    
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