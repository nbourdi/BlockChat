from flask import Flask
import threading
import requests
import logging
from client import CLI
from transaction import Transaction
from api import api, global_node
from node import Node
import os
import sys
import time


bootstrap_ip = '127.0.0.1'
bootstrap_port = 5000
port = 5000

node = global_node


is_bootstrap = os.environ.get('IS_BOOTSTRAP')

ip = '127.0.0.1'

registration_completed = False  # Flag to track registration status


app = Flask(__name__)
app.register_blueprint(api)



stake = 5
capacity = 10

logging.basicConfig(filename='record.log', level=logging.DEBUG)



def register_node1():
    # Wait for a brief period to allow the Flask server to start running
    time.sleep(1)  # Adjust the sleep duration as needed

    json_info = {
        'ip': "127.0.0.1",
        'port': port,
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

    for peer in node.peers:
        if peer.id == 1:
            bootstrap_pk = peer.public_key
    
            # node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="message", amount=None, message="hi bitches")
            # node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="message", amount=None, message="hi bitches")
            # node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="message", amount=None, message="hi bitches")
            # node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="message", amount=None, message="hi bitches")
            # node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="message", amount=None, message="hi bitches")
            # node.create_transaction(receiver_address=bootstrap_pk, type_of_transaction="message", amount=None, message="hi bitches")

    



# def main():
#     print("Node ID:", node.id)
#     print("Node Wallet Public Key:", node.wallet.public_key)
#     print("Node Blockchain Length:", len(node.blockchain.blocks))

if __name__ == "__main__":

    if is_bootstrap == 1:

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

        node.cli = CLI("127.0.0.1", 5000)
        cli_thread = threading.Thread(target=node.cli.start, args=())
        cli_thread.start()
        print(" ============================================================= "
              )
        print(node.wallet.public_key)


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


    else:

        # Start a new thread for registering the node if registration is not completed
        if not registration_completed:
            registration_thread = threading.Thread(target=register_node1)
            registration_thread.start()

        node.cli = CLI("127.0.0.1", port)
        cli_thread = threading.Thread(target=node.cli.start, args=())
        cli_thread.start()
        app.run(ip, port)

        print("\nBlockchain that ive validated\n")
        for block in node.blockchain.blocks:
            print(block)

    print("\ncurr block\n")
    #print(node.curr_block)

