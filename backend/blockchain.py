class Blockchain:

    def __init__(self):
        self.blocks = [] # just a list of all the blocks that are currently validated

    def add_block(self, block):
        self.blocks.append(block)