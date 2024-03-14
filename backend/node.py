
from backend.transaction import Transaction
from backend.wallet import Wallet
from backend.blockchain import Blockchain
from backend.block import Block
import threading

class Peer: # helper class, to represent peer node data
    def __init__(self, peer_id, ip, port, public_key, balance):
        self.id = peer_id
        self.ip = ip
        self.port = port
        self.public_key = public_key
        self.balance = balance
        self.stake = None

class Node:

    def __init__(self, capacity=5, stake=10):
        self.id = None  # node's index/id
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        self.peers = []  # info about other nodes, should be in the [ip, port, pubkey] format, the ring
        self.nonce = 0
        self.curr_block = None  # the current block
        self.peer_stakes = []
        self.q_transactions = [] # list of transactions in queue that belong to the next block
        self.capacity = capacity # idk how we will set this, may just do it manually for each experiment
        self.stake = stake # same question as cap
        #self.capacity = None #Anastasia added this (probably wrong)

        
    def create_transaction(self, receiver_address, type_of_transaction, amount, message):
        trans = Transaction(self.wallet.public_key, receiver_address, type_of_transaction, amount, message)
        trans.sign_transaction(self.wallet.private_key)
        trans.broadcast_transaction(trans)

    def broadcast_transaction(self, trans): # TODO

        # this should broadcast trans to all self.peers
        # need threads for this
        # 
        pass

    def stake(self, stake_amount): # TODO
        # Η συνάρτηση καλείται από τους nodes 
        #για να καθορίσουν το ποσό που δεσμεύουν ως stake για το proof-of-stake
        # Αυτό το ποσό καθορίζει και την πιθανότητα του κόμβου να επιλεγεί ως validator.
        # κάθε validator θα πρέπει να είναι σε θέση να κάνει και update στο ποσό
        # που έχει αποφασίσει να δεσμεύσει.
        # transaction με receiver_address = 0 και το ποσο που θλει να δεσμευσει ο καθε κομβος
        # 
        if self.balance < stake_amount:
            print(f"Can't stake {stake_amount}, not enough BCC in your acount...")
            return False
        else:
            self.stake = stake_amount
            self.create_transaction(0, type_of_transaction="stake", amount=stake_amount, message=None)
            return True
        
    def validate_block(self, block): 
        # validate the previous hash and check validity of current hash
        if block.previous_hash == self.blockchain.blocks[-1].current_hash and block.current_hash == block.hash():
            return True
        return False
    
    def validate_chain(self):
        previous_block = None

        for block in self.blockchain.blocks:
            if block.index == 1:
                if block.previous_hash != 1 or block.current_hash != block.hash():
                    return False
            elif block.index != 0: # genesis block cannot be validated
                if block.previous_hash != previous_block.current_hash or block.current_hash != block.hash():
                    return False
            previous_block = block
        return True

    def send_blockchain_to_peer(self, peer):
        # HTTP POST it to peer.ip, peer.port
        pass
                
    
    def add_peer(self, id, ip, port, public_key, balance):
        # Add peer to ring, probably only called by bootstrap 
        peer = Peer(id, ip, port, public_key, balance)
        self.peers.append(peer)

    def create_block(self): #TODO
        # I'm creating and adding a new block to the blockchain (Anast)
        if len(self.chain.blocks) == 0:
            #genesis block of the chain
            index = 0
            previous_hash = 1
            validator = 0
            capacity = None #not sure about capacity yet, wanna check it out later -Anastasia
            self.curr_block = Block(index, previous_hash, validator, capacity)
            # (Anast) dk yet about capacity
             # #TODO λίστα από transactions περιλαμβάνει μόνο ένα transaction που δίνει στον bootsrap κόμβο 1000*n BCC coins από την wallet διεύθυνση 0
        else:
            self.curr_block = Block(None, None, None, None ) #None values for the time being, gotta check the mining mathod -Anastasia

        return self.curr_block

    def proof_of_stake(self): # TODO 

        #use: need to know who's gonna validate the next block
        #PoS: valivator is based on the ammount of cryptocurrency 
        #every node that wants to validate  uses the stake(amount)
        #method in order to bind the ammount it wants from its wallet 
        #and then 
        amount = input("Enter amount needed for validation") #probably wrong but added for clarity (Anast)
        #gonna check it out later
        s = stake(self, amount)
        


        # i need all peers stakes at this moment
        # then call a random number gen with the same seed for all node instances to get the same result
        # retutn true if im the validator
        # false if not
        # do i need to know which peer is the validator if im not the val?

        ## if validator == me:
        self.mine_block()
        

    def mine_block(self, block): #TODO #not sure if needed, proof of stake method should be the same based on Antoniadis work (Anast)
        # call validator proof of stake competition
        # am i the validator? then i fill in the block fields with the info
        # if i am not the validator? pass?
        pass

    # TODO who is this called by? all nodes or some validator
    # TODO add mutexes if 
    # TODO i want it to return True/False in success, failure. used in api
    def add_to_block(self, transaction):

        if self.curr_block == None: # this only happens when freshly created, right after genesis block
            self.curr_block = self.create_block()

        # check first if self is involved in the transaction
        if (transaction.receiver_address == self.wallet.public_key):
            self.wallet.balance -= transaction.amount
        if (transaction.sender_address == self.wallet.public_key):
            self.wallet.balance += transaction.amount

        # check and update all peers
        for peer in self.peers:
            if peer.public_key == transaction.sender_address:
                peer.balance -= transaction.amount
            if peer.public_key == transaction.receiver_address:
                peer.balance += transaction.amount

        self.curr_block.add_transaction(transaction)

        if self.curr_block.is_full():
            print("Block is full, attempting minting...")
            # Current block is full, initiate mining process
            # call mine competition??
            self.proof_of_stake()
            # if that is successful then empty the queued transactions
            self.q_transactions.clear()
        else:
            print("Transaction is added to queue block, capacity not reached.")
            
        

    # needed for the "view" command in cli, should return last validated block's transactions and the validators id 
    def view_block(self):
        last_block = self.blockchain.blocks[-1]
        return {"validator": last_block.validator, "transactions": last_block.transactions}


        
        

        


        