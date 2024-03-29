from block import Block
from node import Node
from node import Peer
from flask import Blueprint, request, jsonify
import logging

#TO /money LEITOURGEI :D

# Add the path to the backend directory to the Python path
# backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
# sys.path.append(backend_path)
# print(sys.path)

api_blueprint = Blueprint('api', __name__)
node_instance = None

def set_node_instance(node):
    global node_instance
    node_instance = node

app = Blueprint('api', __name__)
n = 3 

# Endpoint to get a block
@app.route('/validate_block', methods=['GET'])
def get_block():

    data = request.get_json()
    inc_block = Block.from_dict(data['Block'])

    # may need lock logic
    if node.validate_block(inc_block):
        # theres def more to it?
        node.blockchain.add_block(inc_block)
        return jsonify({'message': 'Block added successfully'}), 200

    else: # block couldn't be validated
        # if conflict --> resolve conflict
        return jsonify({
            'message': "Block invalid ... Rejected."
        }), 400
    
# Endpoint to get a money
@app.route('/money', methods=['GET'])
def get_money():
    global node_instance
    if node_instance:
        return jsonify({'balance': node_instance.wallet.balance})
    else:
        return jsonify({'error': 'Node instance is not set.'}), 500

# Endpoint to validate a transaction
@app.route('/validate_transaction', methods=['POST'])
def validate_transaction():

    data = request.get_json()
    inc_transaction = Block.from_dict(data['Trabsaction'])

    if node.add_to_block(inc_transaction):
        return jsonify({'message': "Transaction validated successfully."}), 200
    else:
        return jsonify({'message': "Couldn't verify signature, transaction rejected."}), 400
    

# Endpoint to get a transaction, i think this is covered by validate_transaction bc it also adds it if its signature verified 
# @app.route('/add_transaction', methods=['POST'])
# def add_transaction():
#     inc_transaction = json.loads(request.get_data().decode('utf-8')) # incoming transaction
#     if node.add_to_block(inc_transaction):
#         return jsonify({'message': "Transaction added."}), 200
#     else:
#         return jsonify({'message': "Transaction wasn't added."}), 400



# Endpoint to register a node, by bootstrap
@app.route('/register_node', methods=['POST'])
def register_node():
    # Logic to register a node in the network
    peer_pk = request.form.get('public_key')
    peer_ip = request.form.get('ip')
    peer_port = request.form.get('port')
    peer_id = len(node.peers) + 2 # bootstrap is 1 so when node.peers are empty the first peer gets id 2

    # Add node in the list of registered nodes.
    node.add_peer(peer_id, peer_ip, peer_port, peer_pk, 0)
    
    # If all nodes have been added
    if peer_id == n - 1:
        for peer in node.peers:
            if peer.id != node.id:
                node.send_blockchain_to_peer(peer=peer)
                node.send_peer_ring(peer) 
                node.create_transaction(
                    receiver_address=peer.public_key,
                    type_of_transaction="coins",
                    amount=1000,
                    message=None
                )

    return jsonify({'message': "Node added successfully", 'id': peer_id}), 200

# Endpoint to get the ring
@app.route('/get_ring', methods=['POST'])
def get_ring():
    try:
        data = request.get_json()
        peers = [Peer(peer['id'], peer['ip'], peer['port'], peer['public_key'], peer['balance']) for peer in data]
        
        for peer in peers:
            node.add_peer_obj(peer)
        
        return jsonify({"message": "Peers received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

# Endpoint to get the chain
@app.route('/validate_chain', methods=['POST'])
def get_chain():
    try:
        data = request.get_json()
        
        
        node.validate_chain()
        
        return jsonify({"message": "Chain received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
     



# Endpoint to create a transaction
@app.route('/create_transaction', methods=['POST'])
def create_transaction ():
    receiver_id = request.form.get('receiver')
    type_of_transaction = request.form.get('type')

    if type_of_transaction == "coins":
        amount = request.form.get('amount')
    else: 
        message = request.form.get('message')

    # Find the address of the receiver.
    receiver_public_key = None
    for ring_node in node.ring:
        if (ring_node['id'] == receiver_id):
            receiver_public_key = ring_node['public_key']
    if (receiver_public_key and receiver_id != node.id):
        if node.create_transaction(receiver_public_key, receiver_id, amount):
            return jsonify({'message': 'The transaction was successful.', 'balance': node.wallet.get_balance()}), 200
        else:
            return jsonify({'message': 'Not enough NBCs.', 'balance': node.wallet.get_balance()}), 400
    else:
        return jsonify({'message': 'Transaction failed. Wrong receiver id.'}), 4

#  only implement if needed, idk if theyre essential for functionality
# Endpoint to send the chain
# @app.route('/send_chain', methods=['POST'])
# def send_chain():
#     # Logic to send the chain
    
# # Endpoint to get the balance
# @app.route('/get_balance', methods=['GET'])
# def get_balance():
#     # Logic to get balance

# # Endpoint to get transactions
# @app.route('/get_transactions', methods=['GET'])
# def get_transactions():
#     # Logic to get transactions

# # Endpoint to get my transactions
# @app.route('/get_my_transactions', methods=['GET'])
# def get_my_transactions():
#     # Logic to get transactions

# # Endpoint to get ID
# @app.route('/get_id', methods=['GET'])
# def get_id():
#     # Logic to get ID

# # Endpoint to get metrics
# @app.route('/get_metrics', methods=['GET'])
# def get_metrics():
#     # Logic to get metrics
