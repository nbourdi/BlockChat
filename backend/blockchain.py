import json

from block import Block


class Blockchain:

    def __init__(self):
        self.blocks = [] # just a list of all the blocks that are currently validated
        # nonce epifulaksi
       # self.nonce_history = {}  # Ένα λεξικό που θα κρατάει το ιστορικό των nonces ανάλογα με τον λογαριασμό

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

    @classmethod
    def from_json(cls, json_data):
        blockchain = cls()
        blockchain.blocks = [Block.from_json(block) for block in json_data['blocks']]
        return blockchain

    def __str__(self):
        block_strings = [str(block) for block in self.blocks]
        return "\n".join(block_strings)