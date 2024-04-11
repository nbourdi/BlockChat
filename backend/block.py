import hashlib
import json
import time

from transaction import Transaction

'''
Block
 To κάθε block έχει τις εξής πληροφορίες
 ● index:oαύξωναριθμόςτουblock,
 ● timestamp:τοtimestamp της δημιουργίας του block
 ● transactions: Η λίστα με τα transactions που περιέχονται στο block
 ● validator: το public key του κόμβου που επικύρωσε το block
 ● current_hash: το hash του block
 ● previous_hash: το hash του προηγούμενου block στο blockchain.
 Θεωρούμε ότι το κάθε block έχει συγκεριμένη χωρητικότητα σε αριθμό από transaction. Η
 χωρητικότητα καθορίζεται από τη σταθερά capacity.
 
 '''
class Block:

    def __init__(self, index, previous_hash, validator, capacity, current_hash):
        self.index = index # let genesis have index 0 
        self.transactions = []
        self.validator = validator
        self.previous_hash = previous_hash
        self.capacity = capacity  # i added this 
        self.current_hash = current_hash if current_hash else self.hash()

    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.current_hash = self.hash()

    def hash(self):
        block_string = json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'capacity': self.capacity,
            'transactions': [t.to_json() for t in self.transactions]
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'capacity': self.capacity,
            'transactions': [t.to_dict() for t in self.transactions],
            'current_hash': self.current_hash,
        }
    
    def to_json(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'capacity': self.capacity,
            'transactions': [t.to_json() for t in self.transactions],
            'current_hash': self.current_hash,
        }
    
    # def from_dict(cls, block_dict):
    #     block = cls(
    #         index=block_dict['index'],
    #         previous_hash=block_dict['previous_hash'],
    #         validator=block_dict['validator'],
    #         capacity=block_dict['capacity']
    #     )
    #     block.transactions = block_dict['transactions']
    #     block.current_hash = block_dict['current_hash']
    #     block.nonce = block_dict['nonce']
    #     block.timestamp = block_dict['timestamp']
    #     return block

    def from_dict(cls, block_dict):
        block = cls(
            index=block_dict['index'],
            previous_hash=block_dict['previous_hash'],
            validator=block_dict['validator'],
            capacity=block_dict['capacity']
        )
        block.transactions = [Transaction(**tx) for tx in block_dict['transactions']]
        block.current_hash = block_dict['current_hash']
        return block
    
   
    # @classmethod
    # def from_json(cls, json_data):
    #     block = cls(
    #         json_data['index'],
    #         json_data['previous_hash'],
    #         json_data['validator'],
    #         json_data['capacity'],
    #         json_data['current_hash']
    #     )
    #     block.transactions = [Transaction(**tx) for tx in json_data['transactions']]
    #     #block.current_hash = json_data['current_hash']
    #     return block
    
    @classmethod
    def from_json(cls, json_data):
        # print(f"Type of json_data: {type(json_data)}")
        # print(f"Content of json_data: {json_data}")
        
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        block = cls(
            json_data['index'],
            json_data['previous_hash'],
            json_data['validator'],
            json_data['capacity'],
            json_data['current_hash']
        )
        block.transactions = [Transaction(**tx) for tx in json_data['transactions']]
        return block
    
    def __str__(self):
        transaction_strings = [str(tx.amount) for tx in self.transactions]
        transactions_str = "\n    ".join(transaction_strings)
        
        return (
            f"Block {self.index}:\n"
            f"  Previous Hash: {self.previous_hash}\n"
            f"  Validator: {self.validator}\n"
            f"  Capacity: {self.capacity}\n"
            f"  Transactions:\n    {transactions_str}\n"
            f"  Current Hash: {self.current_hash}"
        )