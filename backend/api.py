import base64
from blockchain import Blockchain
from block import Block
from node import Node
from node import Peer
from transaction import Transaction
from flask import Blueprint, request, jsonify
import logging
import json
from transaction import Transaction

logging.basicConfig(filename='record.log', level=logging.DEBUG)

api = Blueprint('api', __name__)
n = 2

global global_node
global_node = Node(1, 10)
node = global_node


# Endpoint to register a node, by bootstrap
@api.route('/register_node', methods=['POST'])
def register_node():
    # Logic to register a node in the network

    data = request.json  # This will contain the JSON data sent via POST
    peer_ip = data.get('ip')
    peer_port = data.get('port')
    peer_pk = data.get('pub_key')
    logging.debug("\n\n\nReceived registration request from peer with IP: %s, Port: %s, pubkey: %s\n\n", peer_ip, peer_port, peer_pk)

    peer_id = len(node.peers) + 1

    # Add node in the list of registered nodes.
    node.add_peer(peer_id, peer_ip, peer_port, peer_pk, 0)
    
    # If all nodes have been added
    if peer_id == n:
        for peer in node.peers:
            if peer.id != node.id:
                node.send_blockchain_to_peer(peer=peer)
                node.send_peer_ring(peer)
                 
        for peer in node.peers:
            if peer.id != node.id:
                node.create_transaction(
                    receiver_address=peer.public_key,
                    type_of_transaction="coins",
                    amount=1000,
                    message=None
                )

    return jsonify({'message': "Node added successfully", 'id': peer_id}), 200

@api.route('/money', methods=['GET'])
def get_money():
    return jsonify({'balance': node.wallet.balance})

# Endpoint to get a block
@api.route('/validate_block', methods=['GET'])
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
        logging.debug("Data that I received:\n%s", data)  # Log the received data
        data = json.loads(data)
        
        peers = [Peer(item['id'], item['ip'], item['port'], item['public_key'], item['balance']) for item in data]
        


        for peer in peers:
            node.add_peer_obj(peer)

        print("HI love the peers u gave me ")
        print("Printing data of peers:")
        for peer in node.peers:
            print(f"Peer ID: {peer.id}")
            print(f"IP Address: {peer.ip}")
            print(f"Port: {peer.port}")
    # You can print additional attributes as needed

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
        
        
        logging.debug("\n\n\n EIMAI STO VALIDATE CHAIN BITCH")
        logging.debug(type(data))
        logging.debug(data)
        
        # Access the blocks key in the data dictionary
        blocks = data.get('blocks', [])
        # Get the existing blockchain instance
        existing_blockchain = node.blockchain

        # Iterate over each block
        for block in blocks:
            # Extract block attributes
            index = block.get('index')
            timestamp = block.get('timestamp')
            previous_hash = block.get('previous_hash')
            nonce = block.get('nonce')
            capacity = block.get('capacity')
            validator = block.get('validator')

            # Access the transactions key in each block
            transactions = block.get('transactions', [])

            # Iterate over each transaction in the transactions list
            for transaction in transactions:
                # Extract transaction attributes
                sender_address = transaction.get('sender_address')
                receiver_address = transaction.get('receiver_address')
                type_of_transaction = transaction.get('type_of_transaction')
                amount = transaction.get('amount')
                nonce = transaction.get('nonce')
                message = transaction.get('message')
                transaction_id = transaction.get('transaction_id')
                signature = transaction.get('signature')
                new_transaction = Transaction(sender_address, receiver_address, type_of_transaction, amount, message, nonce, transaction_id, signature)
                # existing_blockchain.blocks[-1].add_transaction(new_transaction)

                # Now you can modify these variables as needed
                # For example, modify the amount of a transaction
                # Print or use the modified variables as needed

        new_blockchain = Blockchain()
        node.blockchain = new_blockchain

        new_block = node.create_block(index=index, previous_hash=previous_hash, validator=validator, capacity=capacity,timestamp=timestamp)
        node.curr_block = new_block
        node.curr_block.add_transaction(new_transaction)
        node.blockchain.add_block(new_block)
                    
        logging.debug("\n\nExtract blockchain data from JSON")

        # TODO ftiajse to chain apo to data
        # TODO add the blocks in the data to the blockchain

        logging.debug(new_blockchain.blocks[-1])
        
        node.validate_chain() #FIXME δεν εχει κατι συγκεκριμενο απλα δεν ξερω τι κανει οποτε καποτε καποιο καλο κοριτσι να μ εξηγησει
        
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
