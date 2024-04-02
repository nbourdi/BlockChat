from flask import Flask
import requests
import logging
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

stake = 5
capacity = 10

node = Node(capacity=capacity, stake=stake)

logging.basicConfig(filename='record.log', level=logging.DEBUG)

registration_completed = False  # Flag to track registration status


def register_node1():
    # Wait for a brief period to allow the Flask server to start running
    time.sleep(1)  # Adjust the sleep duration as needed

    json_info = {
        'ip': "127.0.0.1",
        'port': "5001",
        'pub_key': node.wallet.public_key
    }

    url = f'http://{bootstrap_ip}:{bootstrap_port}/register_node'
    response = requests.post(url, json=json_info)
    
    try:
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()
        node.id = int(response_data.get('id'))
        print("Registration completed.")
    except Exception as e:
        print(f"Failed to register node: {e}")


if __name__ == "__main__":
    app.logger.debug("im node1 test temp")

    # Start a new thread for registering the node if registration is not completed
    if not registration_completed:
        registration_thread = threading.Thread(target=register_node1)
        registration_thread.start()

    app.run(host="127.0.0.1", port=5001)
