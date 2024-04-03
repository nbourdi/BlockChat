import base64
import json
from random import random
from transaction import Transaction
from wallet import Wallet
from blockchain import Blockchain
from block import Block
import requests
import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG)


class Peer: # helper class, to represent peer node data
    def __init__(self, peer_id, ip, port, public_key, balance):
        self.id = peer_id
        self.ip = ip
        self.port = port
        self.public_key = public_key
        self.balance = balance
        self.stake = None
        self.stake_share = 0
        # self.nonce = 0


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
        self.nonce += 1 #added this (athina)

        trans = Transaction(self.wallet.public_key, receiver_address, type_of_transaction, amount, message, self.nonce) #added the nonce attribute (athina)
        print(trans.signature)
        trans.sign_transaction(self.wallet.private_key)
        print(trans.signature)
        
        self.add_to_block(trans)
        
        self.broadcast_transaction(trans)
        #Am I charged for sending messages? Is this impemented? #TODO (Anast)


    def stake(self, stake_amount): 
        # FIXME stakes should be released when minting is done
        # FIXME stakes should be broadcasted so that they can be updated in Peer object, rn we can bypass by manually staking/releasing
        # Η συνάρτηση καλείται από τους nodes 
        # κάθε validator θα πρέπει να είναι σε θέση να κάνει και update στο ποσό
        # που έχει αποφασίσει να δεσμεύσει.
        # transaction με receiver_address = 0 και το ποσο που θλει να δεσμευσει ο καθε κομβος
        
        if self.balance < stake_amount:
            print(f"Can't stake {stake_amount}, not enough BCC in your acount...")
            return False
        else:
            self.stake = stake_amount
            self.create_transaction(0, type_of_transaction="stake", amount=stake_amount, message=None)
            self.broadcast_stake()
            return True
        
    # TODO last -prio
    def update_stake(self, stake_amount):
        # create a transaction 
        pass

    # TODO high prior
    def release_stakes(self):
        pass
        
    def validate_block(self, block): 
        # validate the previous hash and check validity of current hash
        # TODO last prior εχει και αλλο εδω Επαληθεύεται ότι (a) ο validator είναι πράγματι ο σωστός (αυτός που υπέδειξε η κλήση της
        # ψευδοτυχαίας γεννήτριας)
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

# Inside the Node class in node.py



    def send_blockchain_to_peer(self, peer):
        blocks_json = []
        for block in self.blockchain.blocks:
            transactions = [tx.to_dict() for tx in block.transactions]
            block_data = {
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': transactions,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce
            }
            blocks_json.append(block_data)

        data = {
            'blocks': blocks_json
        }

        address = f"http://{peer.ip}:{peer.port}/validate_chain"
        res = requests.post(address, json=data)
        return res



                
    def add_peer(self, id, ip, port, public_key, balance):
        # Add peer to ring, probably only called by bootstrap 
        peer = Peer(id, ip, port, public_key, balance)
        self.peers.append(peer)

    def add_peer_obj(self, peer: Peer):
        self.peers.append(peer)

    def create_block(self, index, previous_hash, validator, capacity): #TODO
        # I'm creating and adding a new block to the blockchain (Anast)
        if len(self.blockchain.blocks) == 0:
            #genesis block of the chain
            index = 0
            previous_hash = 1
            validator = 0
            self.curr_block = Block(index, previous_hash, validator, capacity)
        else:
            self.curr_block = Block(index, previous_hash, validator, capacity ) #None values for the time being, gotta check the mining mathod -Anastasia | filled (Nat)

        return self.curr_block

    def proof_of_stake(self):

        #use: need to know who's gonna validate the next block
        #PoS: valivator is based on the ammount of cryptocurrency 
        #method in order to bind the ammount it wants from its wallet 
       
        
        validator = -1 # no one validates
        stake_sum = self.stake

        for peer in self.peers:
            stake_sum += peer.stake
        
        share_offset = 0
        for peer in self.peers:
            peer.stake_share = [share_offset, peer.stake / stake_sum + share_offset]
            share_offset += peer.stake

        #  the seed is the hash of the previous block
        seed_hex = self.blockchain.blocks[-1].hash()
        seed = int(seed_hex, 16) # convert to int
        random.seed(seed) # sets the seed for the generator

        # competition
        rand = random()

        for peer in self.peers:
            if peer.stake_share[0] <= rand < peer.stake_share[1]:
                validator = peer.id
                break

        # if i win, i mint
        if validator == self.id:
            print("won the competition, attempting mint,,,")
            self.mint_block()
        
        self.reward(validator) # every node will call this to give the fees to the validator
        
        
    # Ο επικυρωτής του block είναι και αυτός στου οποίου το wallet πιστώνονται οι χρεώσεις των
      # transactions που έχουν συμπεριληφθεί στο block .
    def reward(self, validator_id):

        fee = 0
        for t in self.q_transactions:

            if t.type_of_transaction == "coins":
                fee += 0.03 * t.amount # a 3% fee
            else:
                fee += len(t.message) # 1 char = 1BCC, we do count spaces

        if validator_id == self.id:
            self.wallet.balance += fee
        else:
            for peer in self.peers:
                if peer.id == validator_id:
                    peer.balance += fee


    def mint_block(self):  
        # fill in the block, create if not created
        # curr_block should be None unless there is an error thinking of it, should set back to None once its broadcasted 
        
        if self.curr_block == None:
            self.create_block(index=self.blockchain.blocks[-1].index + 1, previous_hash=self.blockchain.blocks[-1].hash, validator=self.id, capacity=10) # TODO capacity here arbitrary

        self.curr_block.current_hash = self.curr_block.hash()

        transactions = self.q_transactions

        for t in transactions:
            self.curr_block.add_transaction(t)

        # TODO last prior maybe we should have the minter validate his own block or is that redundant like
            # self.validate_block(curr_block ..)

        self.broadcast_block(self.curr_block)
        self.curr_block = None

    # mostly done? are threads necess?, all error handling, get responses?
    def broadcast_block(self, block):

        # data = {'Block': block.to_dict()}
        block_json = json.dumps(block.to_dict())

        # send to every node in peers[]
        for peer in self.peers:
            address = 'http://' + peer.ip + ':' + peer.port + '/validate_block'

            res = requests.post(address, block_json)

            if res.status_code == 200:
                print(f"Block sent to peer with id = {peer.id}")
            else:
                print(f"Error sending to peer with id = {peer.id}")

    def broadcast_transaction(self, trans): 
        # """Εκπέμπει τη συναλλαγή σε όλα τα peer."""
        # data = {'Transaction': transaction.to_dict()}
        print("hii")
        trans_dict = trans.to_dict()
        # print(trans_dict)
        if trans_dict['signature']:
            trans_dict['signature'] = base64.b64encode(trans_dict['signature']).decode('utf-8')
    
        trans_json = json.dumps(trans_dict)
        print("\n\n\n"+trans_json)


        for peer in self.peers:
            address = 'http://' + peer.ip + ':' + peer.port + '/validate_transaction' 
            try:
                res = requests.post(address, json=trans_json)
                if res.status_code == 200:
                    print(f"Transaction successfully sent to {peer.ip}:{peer.port}")
                else:
                    print(f"Failed to send transaction to {peer.ip}:{peer.port}")
            except Exception as e:
                print(f"Error sending transaction to {peer.ip}:{peer.port}: {e}")


    def add_to_block(self, transaction):

        if transaction.verify_signature() == False:
            print("verify sig is false")
            return False
        
        # if self.curr_block == None: # this only happens when freshly created, right after genesis block
        #     self.curr_block = self.create_block()

        # # check first if self is involved in the transaction
        # if (transaction.receiver_address == self.wallet.public_key):
        #     self.wallet.balance -= transaction.amount
        # if (transaction.sender_address == self.wallet.public_key):
        #     self.wallet.balance += transaction.amount

        # # check and update all peers
        # for peer in self.peers:
        #     if peer.public_key == transaction.sender_address:
        #         peer.balance -= transaction.amount
        #     if peer.public_key == transaction.receiver_address:
        #         peer.balance += transaction.amount

        # self.curr_block.add_transaction(transaction)

        # if self.curr_block.is_full():
        #     print("Block is full, attempting minting...")
        #     # Current block is full, initiate mining process
        #     # call mine competition??
        #     self.proof_of_stake()
        #     # if that is successful then empty the queued transactions
        #     self.q_transactions.clear()
        # else:
        #     print("Transaction is added to queue block, capacity not reached.")

        print("after add to block")
        return True
    

    # used by bootstrap to send the whole peer ring to some peer, via HTTP post            
    def send_peer_ring(self, peer):
        ring_data = []
        for peer_node in self.peers:
            peer_data = {
                'id': peer_node.id,
                'ip': peer_node.ip,
                'port': peer_node.port,
                'public_key': peer_node.public_key,
                'balance': peer_node.balance
            }
            ring_data.append(peer_data)

        ring_json = json.dumps(ring_data)

        address = 'http://' + peer.ip + ':' + peer.port + '/get_ring'
        try:
            res = requests.post(address, json=ring_json)
            if res.status_code == 200:
                print(f"Ring successfully sent to {peer.ip}:{peer.port}")
            else:
                print(f"Failed to send ring to {peer.ip}:{peer.port}")
        except Exception as e:
            print(f"Error sending ring to {peer.ip}:{peer.port}: {e}")


    # needed for the "view" command in cli, should return last validated block's transactions and the validators id 
    def view_block(self):
        last_block = self.blockchain.blocks[-1]
        return {"validator": last_block.validator, "transactions": last_block.transactions}


        
        

        


           
