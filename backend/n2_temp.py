from asyncio import sleep
from flask import Flask
import requests
import logging
from client import CLI
from transaction import Transaction
from node import Node
from api import api, global_node
import threading
import time


bootstrap_ip = '127.0.0.1'
bootstrap_port = 5000
node = global_node
is_bootstrap = "1"

ip = '127.0.0.1'

app = Flask(__name__)
app.register_blueprint(api)


#node = Node(capacity=capacity, stake=stake)

logging.basicConfig(filename='record.log', level=logging.DEBUG)

registration_completed = False  # Flag to track registration status


def register_node1():
    # Wait for a brief period to allow the Flask server to start running
    time.sleep(1)  # Adjust the sleep duration as needed

    json_info = {
        'ip': "127.0.0.1",
        'port': "5002",
        'pub_key': node.wallet.public_key
    }

    url = f'http://{bootstrap_ip}:{bootstrap_port}/get_id'
    response = requests.post(url, json=json_info)
    
    try:
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()
        node.id = int(response_data.get('id'))
        print("Got id.")
    except Exception as e:
        print(f"Failed to get id for node: {e}")

    json_info = {
        'id': node.id
    }
    url = f'http://{bootstrap_ip}:{bootstrap_port}/register_node'
    response = requests.post(url, json=json_info)
    try:
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()
        print("Registration complete")
    except Exception as e:
        print(f"Failed to register node: {e}")
    
    while not node.bootstraping_done:
        pass
    
    for peer in node.peers:
        print(f"going through peers: ")
        if peer.id == 2:
            bootstrap_pk = peer.public_key

            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=1, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=2, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=3, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=4, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=5, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=6, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=31, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=32, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=33, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=34, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=35, message=None)
            node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="coins", amount=36, message=None)

    

if __name__ == "__main__":
    app.logger.debug("im node1 test temp")


    # Start a new thread for registering the node if registration is not completed
    if not registration_completed:
        registration_thread = threading.Thread(target=register_node1)
        registration_thread.start()
    node.cli = CLI("127.0.0.1", 5000)
    cli_thread = threading.Thread(target=node.cli.start, args=())
    cli_thread.start()
    app.run(host="127.0.0.1", port=5002)
    
    print("\n\ Blockchain that ive validated\n")
    for block in node.blockchain.blocks:
        print(block)
