from flask import Flask
import requests
from node import Node
from api import app 

bootstrap_ip = '127.0.0.1'
bootstrap_port = 3001

ip = '127.0.0.1'

appp = Flask(__name__)
appp.register_blueprint(app)

stake = 5
capacity = 10

node1 = Node(capacity=capacity, stake=stake)

def main():
    print("Node ID:", node1.id)
    print("Node Wallet Public Key:", node1.wallet.public_key)
    print("Node Blockchain Length:", len(node1.blockchain.blocks))

if __name__ == "__main__":

    print("Do you wanna be bootstrap??? 1 for yes, 0 for no...\n")
    bool = int(input())
    print("Give port to run node on:")
    port = int(input())

    appp.run(ip, port)

    json_info = {
        'ip': "127.0.0.1",
        'port': port,
        'pub_key': node1.wallet.public_key
    }
    print(json_info)

    url = f'http://{bootstrap_ip}:{bootstrap_port}/register_node'
    response = requests.post(url, json=json_info)
    response_data = response.json()

    node1.id = int(response_data['id'])
    
    main()
