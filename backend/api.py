import base64
from blockchain import Blockchain
from block import Block
from node import Node
from node import Peer
from flask import Blueprint, request, jsonify
import logging
import json
from transaction import Transaction

logging.basicConfig(filename='record.log', level=logging.DEBUG)

api = Blueprint('api', __name__)
n = 3

global global_node
global_node = Node(2, 10)
node = global_node

@api.route('/get_id', methods=['POST'])
def get_id():
    data = request.json
    peer_ip = data.get('ip')
    peer_port = data.get('port')
    peer_pk = data.get('pub_key')
    logging.debug("\n\n\nReceived registration request from peer with IP: %s, Port: %s, pubkey: %s\n\n", peer_ip, peer_port, peer_pk)

    peer_id = len(node.peers) + 1

    # Add node in the list of registered nodes.
    node.add_peer(peer_id, peer_ip, peer_port, peer_pk, 0)

    response_data = {'message': "Node added successfully", 'id': peer_id}
    return jsonify(response_data), 200

# Endpoint to register a node, by bootstrap
@api.route('/register_node', methods=['POST'])
def register_node():
    data = request.json
    peer_id = data.get('id')

    # If all nodes have been added
    if peer_id == n:
        for peer in node.peers:
            if peer.id != node.id:
                node.send_blockchain_to_peer(peer=peer)
                node.send_peer_ring(peer) 
        node.curr_block = None
        for peer in node.peers:
            if peer.id != node.id:
                logging.debug("\n\n ====================== CREATING REG TRANSACTION............")
                node.create_transaction(
                    receiver_address=peer.public_key,
                    type_of_transaction="coins",
                    amount=1000,
                    message=None
                )
                
    logging.debug("line 52 blockchain at register, boot strap:")
    logging.debug(node.blockchain)

    return jsonify({"message": "Registered all nodes"}), 200


@api.route('/money', methods=['GET'])
def get_money():
    return jsonify({'balance': node.wallet.balance})

# Endpoint to get a block
@api.route('/validate_block', methods=['POST'])
def get_block():

    data = request.get_json()
    logging.debug("line 65 api data for validate block:")
    logging.debug(data)
    inc_block = Block.from_json(data)

    logging.debug("line 69 inc block index:::")
    logging.debug(inc_block.index)
    logging.debug(inc_block.validator)

    # may need lock logic
    if node.validate_block(inc_block):
        logging.debug("validate block is true...")
        # theres def more to it?
        node.blockchain.add_block(inc_block)
        node.reward(inc_block.validator)
        node.curr_block = None
        return jsonify({'message': 'Block added successfully'}), 200

    else: # block couldn't be validated
        # if conflict --> resolve conflict
        logging.debug("validate block was false, line 81")
        return jsonify({
            'message': "Block invalid ... Rejected."
        }), 400
    

# Endpoint to validate a transaction
@api.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()

    #logging.debug("Type of data: %s", type(data))  # Log the type of data
    logging.debug("Data that I received:\n%s", data)  # Log the received data


    # Iterate over the list of transactions in the data
    data_dict = json.loads(data)
    #logging.debug("Type of data_dict: %s", type(data_dict))  # Log the type of data
    logging.debug("Data_dict that I received:\n%s", data_dict)  # Log the received data


    sender_address = data_dict['sender_address']
    receiver_address = data_dict['receiver_address']
    type_of_transaction = data_dict['type_of_transaction']
    amount = data_dict['amount']
    nonce = data_dict['nonce']
    message = data_dict['message']
    transaction_id = data_dict['transaction_id']

    # Convert the base64 string signature back to a byte string
    if data_dict['signature']:
        data_dict['signature'] = base64.b64decode(data_dict['signature'])
    signature = data_dict['signature']
    #print("\n\nAFTER ENCODE\n\n")
    #print(signature)

    trans = Transaction(sender_address=sender_address, receiver_address=receiver_address,
                         type_of_transaction=type_of_transaction, amount=amount,
                         message=message, nonce=nonce, transaction_id=transaction_id,signature=signature)
         # Validate the transaction and add it to the block
    # this is wrong we need to add it to the queue not to the block

    if node.add_to_block(trans):
        return jsonify({'message': "Transaction validated successfully."}), 200
    else:
        return jsonify({'message': "Couldn't verify signature, transaction rejected."}), 400


# Endpoint to get the ring
@api.route('/get_ring', methods=['POST'])
def get_ring():
    try:
        data = request.get_json()

        #logging.debug("Type of data: %s", type(data))  # Log the type of data
        #logging.debug("Data that I received:\n%s", data)  # Log the received data
        data = json.loads(data)
        
        peers = [Peer(item['id'], item['ip'], item['port'], item['public_key'], item['balance']) for item in data]
        
        #print(peers)

        for peer in peers:
            node.add_peer_obj(peer)
        
        return jsonify({"message": "Peers received successfully"}), 200
    except Exception as e:
        logging.error("Error occurred while processing JSON data: %s", str(e))
        return jsonify({"error": str(e)}), 400

# @api.route('/get_ring', methods=['POST'])
# def get_ring():
#     try:
#         data = request.get_json()

#         #logging.debug("Type of data: %s", type(data))  # Log the type of data
#         logging.debug("Data that I received:\n%s", data)  # Log the received data
#         data_dict = json.loads(data)
#         for item in data_dict:
#             peer_id = item['id']
#             ip = item['ip']
#             port = item['port']
#             public_key = item['public_key']
#             balance = item['balance']

#         peers = [Peer(peer_id, ip, port, public_key, balance) for item in data]
#         print(len(peers))

#         for peer in peers:
#             node.add_peer_obj(peer)
        

#         return jsonify({"message": "Peers received successfully"}), 200
#     except Exception as e:
#         logging.error("Error occurred while processing JSON data: %s", str(e))
#         return jsonify({"error": str(e)}), 400


    
# Endpoint to get the chain
@api.route('/validate_chain', methods=['POST'])
def get_chain():
    try:
        data = request.get_json()

        chain = Blockchain.from_json(data)
        node.blockchain = chain
        logging.debug("line 187 chain that i validate:")
        logging.debug(chain)
        
        if node.validate_chain():
            return jsonify({"message": "Chain received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
     

# Endpoint to create a transaction
@api.route('/create_transaction', methods=['POST'])
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
