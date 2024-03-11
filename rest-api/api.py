from backend.node import Node
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

node = Node()

# Endpoint to get a block
@app.route('/validate_block', methods=['GET'])
def get_block():
    # Logic to retrieve a block

    inc_block = json.loads(request.get_data().decode('utf-8')) # incoming block

    # may need lock logic
    if node.validate_block(inc_block) == True:
        #TODO theres def more to it
        node.blockchain.add_block(inc_block)

    else: # block couldn't be validated
        # if conflict --> resolve conflict
        # else
        return jsonify({
            'message': "Block invalid... Rejected."
        }), 400



    

# Endpoint to validate a transaction
@app.route('/validate_transaction', methods=['POST'])
def validate_transaction():
    # Logic to validate a transaction

# Endpoint to get a transaction
@app.route('/get_transaction', methods=['GET'])
def get_transaction():
    # Logic to retrieve a transaction

# Endpoint to register a node
@app.route('/register_node', methods=['POST'])
def register_node():
    # Logic to register a node

# Endpoint to get the ring
@app.route('/get_ring', methods=['GET'])
def get_ring():
    # Logic to retrieve the ring

# Endpoint to get the chain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    # Logic to retrieve the chain
    return jsonify(blockchain)

# Endpoint to send the chain
@app.route('/send_chain', methods=['POST'])
def send_chain():
    # Logic to send the chain

# Endpoint to create a transaction
@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    # Logic to create a transaction

# Endpoint to get the balance
@app.route('/get_balance', methods=['GET'])
def get_balance():
    # Logic to get balance

# Endpoint to get transactions
@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    # Logic to get transactions

# Endpoint to get my transactions
@app.route('/get_my_transactions', methods=['GET'])
def get_my_transactions():
    # Logic to get transactions

# Endpoint to get ID
@app.route('/get_id', methods=['GET'])
def get_id():
    # Logic to get ID

# Endpoint to get metrics
@app.route('/get_metrics', methods=['GET'])
def get_metrics():
    # Logic to get metrics

if __name__ == '__main__':
    app.run(debug=True)
