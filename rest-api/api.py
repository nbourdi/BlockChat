from backend.block import Block
from backend.node import Node
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
n = 0 # TODO
node = Node()

# Endpoint to get a block
@app.route('/validate_block', methods=['GET'])
def get_block():
    # Logic to retrieve a block

    data = request.get_json()
    inc_block = Block.from_dict(data['Block'])

    # may need lock logic
    if node.validate_block(inc_block):
        #TODO theres def more to it
        node.blockchain.add_block(inc_block)
        return jsonify({'message': 'Block added successfully'}), 200

    else: # block couldn't be validated
        # if conflict --> resolve conflict
        return jsonify({
            'message': "Block invalid ... Rejected."
        }), 400
    
    
    return jsonify({'message': "Block added to blockchain."}), 200


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



# Endpoint to register a 
# TODO
@app.route('/register_node', methods=['POST'])
def register_node():
    # Logic to register a node as a peer

    peer_pk = request.form.get('public_key')
    peer_ip = request.form.get('ip')
    peer_port = request.form.get('port')
    peer_id = len(node.peers)

    # Add node in the list of registered nodes.
    node.add_peer(peer_id, peer_ip, peer_port, peer_pk, 0)
    
    # If all nodes have been added
    if peer_id == n - 1:
        for peer in node.peers:
            if peer.id != node.id:
                node.send_blockchain_to_peer(peer=peer)
                node.send_peer_ring(peer) # TODO
                node.create_transaction(
                    receiver_address=peer.public_key,
                    type_of_transaction="coins",
                    amount=1000,
                    message=None
                )

    return jsonify({'message': "Node added successfully", 'id': peer_id}), 200

# Endpoint to get the ring... TODO 
# @app.route('/get_ring', methods=['GET'])
# def get_ring():
    # Logic to retrieve the ring

# TODO: only implement if needed, idk if theyre essential for functionality
# Endpoint to get the chain

# NEEDED
# @app.route('/validate_chain', methods=['POST'])
# def get_chain():
#     # Logic to retrieve the chain
#     return jsonify(blockchain)

# Endpoint to send the chain
# @app.route('/send_chain', methods=['POST'])
# def send_chain():
#     # Logic to send the chain

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

if __name__ == '__main__':
    app.run(debug=True)
