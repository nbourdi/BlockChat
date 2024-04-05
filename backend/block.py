import hashlib
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

    def __init__(self, index, previous_hash, validator, capacity,timestamp=None):
        self.index = index # let genesis have index 0 
        self.timestamp = timestamp if timestamp else time.time()
        self.transactions = []
        self.validator = validator
        self.current_hash = None
        self.nonce = None #TODO i dont think it needs nonce?
        self.previous_hash = previous_hash
        self.capacity = capacity  # i added this 
        
    def is_full(self):
        print("block cap")
        print(self.capacity)
        if len(self.transactions) < self.capacity:
            return False
        return True
    
    def __str__(self):
        block_str = f"Block Index: {self.index}\n"
        block_str += f"Timestamp: {self.timestamp}\n"
        block_str += "Transactions:\n"
        for transaction in self.transactions:
            block_str += f"{transaction}\n"
        block_str += f"Validator: {self.validator}\n"
        block_str += f"Current Hash: {self.current_hash}\n"
        block_str += f"Previous Hash: {self.previous_hash}\n"
        block_str += f"Capacity: {self.capacity}\n"
        return block_str
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.validator}{self.previous_hash}{self.capacity}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'capacity': self.capacity,
            'transactions': self.transactions,
            'current_hash': self.current_hash,
            'nonce': self.nonce,
            'timestamp': self.timestamp
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
        block.nonce = block_dict['nonce']
        block.timestamp = block_dict['timestamp']
        return block
    
    
    @classmethod
    def from_json(cls, json_data):
        transactions = [Transaction.from_json(tx) for tx in json_data['transactions']]
        return cls(
            json_data['index'],
            json_data['previous_hash'],
            json_data['validator'],
            json_data['capacity']
        )
    
