import json

from block import Block


class Blockchain:

    def __init__(self):
        self.blocks = [] # just a list of all the blocks that are currently validated
        # nonce epifulaksi
       # self.nonce_history = {}  # Ένα λεξικό που θα κρατάει το ιστορικό των nonces ανάλογα με τον λογαριασμό



    def __str__(self):
        blockchain_info = ""
        for index, block in enumerate(self.blocks):
            blockchain_info += f"Block {index + 1}:\n"
            blockchain_info += f"Index: {block.index}\n"
            blockchain_info += f"Timestamp: {block.timestamp}\n"
            blockchain_info += f"Transactions:\n"
            for transaction in block.transactions:
                blockchain_info += f"    {transaction}\n"
            blockchain_info += f"Validator: {block.validator}\n"
            blockchain_info += f"Current Hash: {block.current_hash}\n"
            blockchain_info += f"Previous Hash: {block.previous_hash}\n\n"
        return blockchain_info
    
    def add_block(self, block):
        self.blocks.append(block)

    def to_dict(self):
        return {
            'blocks': [block.to_dict() for block in self.blocks]
        }

    def to_json(self):
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_data):
        blockchain = cls()
        blockchain.blocks = [Block.from_json(block) for block in json_data['blocks']]
        return blockchain


#  TODO immed erwtisi: auto mipws einai gia to transaction class? to blockchain einai mono 1 opote de xreiazetai nonce (nat)
    # def add_nonce(self, account_address, nonce):
    #     if account_address not in self.nonce_history:
    #         self.nonce_history[account_address] = set()
    #     self.nonce_history[account_address].add(nonce)    

    # def is_nonce_used(self, account_address, nonce):
    #     return nonce in self.nonce_history.get(account_address, set())
    @classmethod
    def from_json(cls, json_data):
        blockchain = cls()
        blockchain.blocks = [Block.from_json(block) for block in json_data['blocks']]
        return blockchain
