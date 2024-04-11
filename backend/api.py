from asyncio import sleep
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
global_node = Node(3, 10)
node = global_node

@api.route('/get_id', methods=['POST'])
def get_id():
    data = request.json
    peer_ip = data.get('ip')
    peer_port = data.get('port')
    peer_pk = data.get('pub_key')
    peer_id = len(node.peers) + 1

    # Add node in the list of registered nodes.
    node.add_peer(peer_id, peer_ip, peer_port, peer_pk, 0, node.stake)

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

        for peer in node.peers:
            if peer.id != node.id:
                logging.debug("\n\n ====================== CREATING REG TRANSACTION............")
                node.create_reg_transaction(
                    receiver_address=peer.public_key,
                    reg_capacity=n-1
                )

    return jsonify({"message": "Registered all nodes"}), 200


@api.route('/money', methods=['GET'])
def get_money():
    return jsonify({'balance': node.wallet.balance})

@api.route('/pending_money', methods=['GET'])
def pending_money():
    return jsonify({'balance': node.unvalidated_balance})

@api.route('/bootstraping_done', methods=['POST'])
def bootstraping_done():
    node.bootstraping_done = True
    return jsonify({'message': "notified"}), 200

# Endpoint to get a block
@api.route('/add_block', methods=['POST'])
def get_block():

    data = request.get_json()
    inc_block = Block.from_json(data)

    if node.validate_block(inc_block):
        # print("ADDING BLOCK BECAUSE IT WAS BROADCASTED TO ME")
        node.blockchain.add_block(inc_block)
        node.finalize_balances(inc_block)
        if node.id == 1 and inc_block.index == 1:
            for peer in node.peers:
                node.notify_reg_complete(peer)

        return jsonify({'message': 'Block added successfully'}), 200
    
    else: # block couldn't be validated
        logging.debug("validate block was false, line 81")
        return jsonify({
            'message': "Block invalid ... Rejected."
        }), 400
    

# Endpoint to validate a transaction
@api.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    data_dict = json.loads(data)
    logging.debug("Data_dict that I received:\n%s", data_dict)  # Log the received data

    sender_address = data_dict['sender_address']
    receiver_address = data_dict['receiver_address']
    type_of_transaction = data_dict['type_of_transaction']
    amount = data_dict['amount']
    nonce = data_dict['nonce']
    message = data_dict['message']
    transaction_id = data_dict['transaction_id']
    if data_dict['signature']:
        data_dict['signature'] = base64.b64decode(data_dict['signature'])
    signature = data_dict['signature']

    trans = Transaction(sender_address=sender_address, receiver_address=receiver_address,
                         type_of_transaction=type_of_transaction, amount=amount,
                         message=message, nonce=nonce, transaction_id=transaction_id,signature=signature)
         

    valid = False
    if trans.type_of_transaction == "coins_reg":
        valid = node.validate_transaction(trans, n-1)

    else:
        valid = node.validate_transaction(trans, node.capacity)
    if valid:
        return jsonify({'message': "Transaction validated successfully."}), 200
    else:
        return jsonify({'message': "Couldn't verify signature, transaction rejected."}), 400


# Endpoint to get the ring
@api.route('/get_ring', methods=['POST'])
def get_ring():
    try:
        data = request.get_json()
        data = json.loads(data)
        
        peers = [Peer(item['id'], item['ip'], item['port'], item['public_key'], item['balance'], item['initial_stake']) for item in data]


        for peer in peers:
            node.add_peer_obj(peer)
        
        return jsonify({"message": "Peers received successfully"}), 200
    except Exception as e:
        logging.error("Error occurred while processing JSON data: %s", str(e))
        return jsonify({"error": str(e)}), 400

    
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
     


    

    ###TODO auto einai mono gia message 
@api.route('/stake', methods=['POST'])
def stake():
    data = request.get_json()
    stake_amount = data.get('stake_amount')
    stake_amount_int = int(stake_amount)
    node.update_stake(stake_amount_int)
    return jsonify({'message': f'Successfully received stake_amount: {stake_amount}'})
    

@api.route('/view', methods=['GET'])
def view():
    block_details = node.view_block()  # Assuming view_block is a standalone function

    if block_details is None:
        return jsonify({'message': 'No blocks validated yet'})

    index = block_details["index"]
    validator = block_details["validator"]
    transactions = block_details["transactions"]

    print("Validator:", validator)
    print("Block Index:", index)
    print("Transactions of the Block:")
    
    for data in transactions:
        print("Transaction ID:", data['transaction_id'])
        print("Sender's ID:", data['sender_address'])
        print("Receiver's ID:", data['receiver_address'])
        print("Type of Transaction:", data['type_of_transaction'])
        print("Amount:", data['amount'])
        print("Message:", data['message'])
        print()

    return jsonify({'message': f'Successfully received stake_amount: {block_details}'})


@api.route('/create_transaction', methods=['POST'])
def create_transaction ():

    receiver_id = request.form.get('receiver')
    receiver_id = int(receiver_id)
    
    sorted_peers = sorted(node.peers, key=lambda x: x.id)
    
    key = sorted_peers[receiver_id-1].public_key
 
    type_of_transaction = request.form.get('type')
    if type_of_transaction == "coins":
        amount = request.form.get('amount')
        amount = int(amount)
    else: 
        message = request.form.get('message')

   # print("WHATS MY MESSAGE?")
   # print(message)
    if type_of_transaction == "message":
        if (key and key != node.wallet.public_key):
            try:
                node.create_transaction(receiver_address=key, type_of_transaction="message", amount=None,message=message)
                return jsonify({'message': 'Message sent succesfully.'}), 200

            except:
                return jsonify({'message': 'Transaction failed.'}), 400
    else:
        if (key and key != node.wallet.public_key):
            try:
                node.create_transaction(receiver_address=key, type_of_transaction="coins", amount=amount,message=None)
                return jsonify({'message': 'Transaction completed successfully.'}), 200

            except:
                print("neyyy")
                return jsonify({'message': 'Transaction failed.'}), 400
