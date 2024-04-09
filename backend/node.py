import base64
import json
import random
import threading
from transaction import Transaction
from wallet import Wallet
from blockchain import Blockchain
from block import Block
import requests
import logging
from client import CLI

logging.basicConfig(filename='record.log', level=logging.DEBUG)


class Peer: # helper class, to represent peer node data
    def __init__(self, peer_id, ip, port, public_key, balance):
        self.id = peer_id
        self.ip = ip
        self.port = port
        self.public_key = public_key
        self.balance = balance
        self.stake = 10 #TODO make it global ALSO #FIXME these wont get into the block more correct to stake in genesis after registration and then broadcast it but we dont have the function 
        self.stake_share = 0
        self.unvalidated_balance = balance
        # self.nonce = 0 # TODO


class Node:

    def __init__(self, capacity, stake):
        self.id = None  # node's index/id
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        self.peers = []  # info about other nodes, should be in the [ip, port, pubkey] format, the ring IN PEER OBJECTS
        self.nonce = 0
        self.peer_stakes = []
        self.q_transactions = [] # list of transactions in queue 
        self.capacity = capacity 
        self.stake = stake 
        self.seen = set()
        self.unvalidated_balance = 0 
        
        # for CLI
        
        
        
    def create_transaction(self, receiver_address, type_of_transaction, amount, message):
        self.nonce += 1 #added this (athina)
        trans = Transaction(self.wallet.public_key, receiver_address, type_of_transaction, amount, message, self.nonce) #added the nonce attribute (athina)
        trans.sign_transaction(self.wallet.private_key)
        self.broadcast_transaction(trans, self.capacity)

    def create_reg_transaction(self, receiver_address, reg_capacity): #TODO could be cleaner
        self.nonce += 1 #added this (athina)
        trans = Transaction(self.wallet.public_key, receiver_address, "coins_reg", 1000, None, self.nonce) #added the nonce attribute (athina)
        trans.sign_transaction(self.wallet.private_key)
        self.broadcast_transaction(trans, reg_capacity)
        return trans
    
    def validate_block(self, block): 
        # validate the previous hash and check validity of current hash
        print("INCOMING BLOCK")
        if block.validator != self.validator_id(block.previous_hash):
            return False
        if block.previous_hash == self.blockchain.blocks[-1].current_hash and block.current_hash == block.hash():
            for t in block.transactions:
                self.seen.add(t.transaction_id) # if i validate a block that i havent had even the chance to pos yet
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
        blocks_json = []
        for block in self.blockchain.blocks:
            transactions = [tx.to_dict() for tx in block.transactions]
            # print("line 98")
            # print(transactions)
            block_data = {
                'index': block.index,
                'transactions': transactions,
                'previous_hash': block.previous_hash,
                'capacity': block.capacity,
                'validator': block.validator,
                'current_hash': block.current_hash
            }
            blocks_json.append(block_data)

        data = {'blocks': blocks_json}

        res = requests.post(f"http://{peer.ip}:{peer.port}/validate_chain", json=data)
        return res


    def add_peer(self, id, ip, port, public_key, balance):
        peer = Peer(id, ip, port, public_key, balance)
        self.peers.append(peer)

    def add_peer_obj(self, peer: Peer):
        self.peers.append(peer)

    def create_block(self, index, previous_hash, validator, capacity, current_hash): 
        # I'm creating and adding a new block to the blockchain (Anast)
        if len(self.blockchain.blocks) == 0:
            #genesis block of the chain - #TODO this will never happen
            index = 0
            previous_hash = 1
            validator = 0
            new_block = Block(index, previous_hash, validator, capacity, current_hash=None)
        else:
            new_block = Block(index, previous_hash, validator, capacity, current_hash=None) #None values for the time being, gotta check the mining mathod -Anastasia | filled (Nat)

        return new_block

    def validator_id(self, seed):
        stake_sum = self.stake

        for peer in self.peers:
            if peer.id != self.id:
                stake_sum += peer.stake
        
        share_offset = 0
        for peer in self.peers:
            peer.stake_share = [share_offset, peer.stake / stake_sum + share_offset]
            share_offset = peer.stake_share[1]

        #  the seed is the hash of the previous block
        seed_hex = seed
        seed = int(seed_hex, 16)  # convert to int

        random_generator = random.Random()
        random_generator.seed(seed)  # set the seed for the random generator

        # competition
        rand = random_generator.random() 

        print(f"==== THE RANDOM NUMBER IS {rand}")
        for peer in self.peers:

            if peer.stake_share[0] <= rand < peer.stake_share[1]:
                return peer.id

    def proof_of_stake(self):

        print(f"\n\n=== ENTERING PROOF OF STAKE WITH STAKE {self.stake}\n\n")
        validator = self.validator_id(self.blockchain.blocks[-1].hash())
        
        
        #self.curr_block.validator = validator
        # if i win, i mint
        if validator == self.id:
            print("====== I WON the competition, MINTING...\n")
            self.mint_block()
            #self.reward(validator)
        else:
            print(f"====== {validator} won the competition\n")
        
         # every node will call this to give the fees to the validator
        
        
    # Ο επικυρωτής του block είναι και αυτός στου οποίου το wallet πιστώνονται οι χρεώσεις των
      # transactions που έχουν συμπεριληφθεί στο block .
    def finalize_balances(self, block):

        print("=====REWARDING THE MINTER & FINALIZING BALANCES..")

        fee = 0
        for t in block.transactions:
            if t.type_of_transaction == "message":
                fee += len(t.message) # 1 char = 1BCC, we do count spaces

            elif t.type_of_transaction == "coins" or t.type_of_transaction == "coins_reg":

                fee += 0.03 * t.amount # a 3% fee
                if t.receiver_address == self.wallet.public_key:
                    self.wallet.balance += t.amount
                if t.sender_address == self.wallet.public_key:
                    self.wallet.balance -= t.amount + t.amount*0.03

                # check and update all peers
                for peer in self.peers:
                    if peer.public_key == t.sender_address:
                        peer.balance -= t.amount + t.amount*0.03
                    if peer.public_key == t.receiver_address:
                        peer.balance += t.amount 

            elif t.type_of_transaction == "stake":

                if t.sender_address == self.wallet.public_key:
                    self.stake -= t.amount
                for peer in self.peers:
                    if t.sender_address == peer.public_key:
                        peer.stake = t.amount

        if block.validator == self.id:
            self.wallet.balance += fee
        else:
            for peer in self.peers:
                if peer.id == block.validator:
                    peer.balance += fee

        # set temporary balances to the new validated ones
        self.unvalidated_balance = self.wallet.balance

        for peer in self.peers:
            peer.unvalidated_balance = peer.balance


    def mint_block(self):  

        transactions = self.q_transactions

        minted_block = self.create_block(
            index=self.blockchain.blocks[-1].index + 1, 
            previous_hash=self.blockchain.blocks[-1].current_hash,
            validator=self.id,
            capacity=self.capacity,
            current_hash=None
            )
        
        for tran in transactions:
            minted_block.add_transaction(tran)
        
        print("===== BROADCASTING THE BLOCK I AM MINTING...: \n\n")
        print(minted_block)
        self.broadcast_block(minted_block)
        self.finalize_balances(minted_block)

    # mostly done? are threads necess?, all error handling, get responses?
    def broadcast_block(self, block):

        block_json = json.dumps(block.to_json())
        lock = threading.Lock()  # Create a lock

        all_validated = True
        def send_block_to_peer(peer):
            nonlocal block_json, all_validated
            address = f'http://{peer.ip}:{peer.port}/add_block'
            try:
                res = requests.post(address, json=block_json)
                if res.status_code == 200:
                    with lock:
                        print(f"Block sent to peer with id = {peer.id}")
                else:
                    with lock:
                        print(f"Error sending to peer with id = {peer.id}")
                        all_validated = False
            except Exception as e:
                with lock:
                    print(f"Error sending block to {peer.ip}:{peer.port}: {e}")
                    all_validated = False
            
            

        threads = []
        for peer in self.peers:
            if peer.id != self.id:
                thread = threading.Thread(target=send_block_to_peer, args=(peer,))
                threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        if all_validated:
            print("ADDING BLOCK BECAUSE I BROADCASTED")
            self.blockchain.add_block(block)

    def broadcast_transaction(self, trans, capacity): 
        """Εκπέμπει τη συναλλαγή σε όλα τα peer."""
        trans_dict = trans.to_dict()

        if trans_dict['signature']:
            trans_dict['signature'] = base64.b64encode(trans_dict['signature']).decode('utf-8')
    
        trans_json = json.dumps(trans_dict)
        lock = threading.Lock()  # Create a lock

        valid_by_all = True

        def send_to_peer(peer):
            nonlocal trans_json, valid_by_all
            address = f'http://{peer.ip}:{peer.port}/add_transaction'
            try:
                res = requests.post(address, json=trans_json)
                if res.status_code == 200:
                    with lock:
                        print(f"Transaction successfully sent to {peer.ip}:{peer.port}")
                else:
                    with lock:
                        print(f"Failed to send transaction to {peer.ip}:{peer.port}")
                        valid_by_all = False
            except Exception as e:
                with lock:
                    print(f"Error sending transaction to {peer.ip}:{peer.port}: {e}")
                    valid_by_all = False

        threads = []
        for peer in self.peers:
            if peer.id != self.id:
                thread = threading.Thread(target=send_to_peer, args=(peer,))
                threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        if valid_by_all:
            self.validate_transaction(trans, capacity)
            #self.q_transactions.append(trans)

        #        if (trans.receiver_address == self.wallet.public_key):
        #     self.wallet.balance += trans.amount
        # if (trans.sender_address == self.wallet.public_key):
        #     self.wallet.balance -= trans.amount

        # # check and update all peers
        # for peer in self.peers:
        #     if peer.public_key == trans.sender_address:
        #         peer.balance -= trans.amount
        #     if peer.public_key == trans.receiver_address:
        #         peer.balance += trans.amount

    
    def add_transaction(self, trans, capacity):
        self.q_transactions.append(trans)

        if (trans.receiver_address == self.wallet.public_key):
            self.unvalidated_balance += trans.amount
        if (trans.sender_address == self.wallet.public_key):
            self.unvalidated_balance -= trans.amount + trans.amount*0.03 # fee is charged to the sender

        # check and update all peers
        for peer in self.peers:
            if peer.public_key == trans.sender_address:
                peer.unvalidated_balance -= trans.amount + trans.amount*0.03
            if peer.public_key == trans.receiver_address:
                peer.unvalidated_balance += trans.amount

        if len(self.q_transactions) == capacity:
            self.proof_of_stake()
            self.q_transactions.clear()
        else:
            print(f"Transaction of {trans.amount} is added to queue block, capacity not reached.")
        

    def validate_transaction(self, t, capacity):

        if t.verify_signature() == False:
            return False
        if t.transaction_id in self.seen:
            return True
        
        if t.sender_address == self.wallet.public_key:
            if self.unvalidated_balance < t.amount*1.03:
                return False
            
        for peer in self.peers:
            if peer.public_key == t.sender_address:
                if peer.unvalidated_balance < t.amount*1.03:
                    return False
        
        self.add_transaction(t, capacity)
        return True
        #TODO high priority ! we also need to check for sufficient funds considering stake too

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

        if peer.id != self.id:
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
    


        
        

        

    def stake(self, stake_amount): 
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

    # TODO mid prior
    def broadcast_stake(self, stake):
        pass
           
#def add_to_block(self, transaction):

    #     print("==== ADD TO BLOCK CALLED")
    #     self.validate_transaction(transaction)
        
    #     if self.curr_block == None: # this only happens when freshly created, right after genesis block?? are you sure
    #         print("do i create rn.?\n")
    #         self.curr_block = self.create_block(index=self.blockchain.blocks[-1].index + 1, previous_hash=self.blockchain.blocks[-1].current_hash, validator=-1, capacity=self.capacity, current_hash=None)

    #     # check first if self is involved in the transaction

    #    # print(self.wallet.public_key)
    #     if (transaction.receiver_address == self.wallet.public_key):
    #         self.wallet.balance += transaction.amount
    #     if (transaction.sender_address == self.wallet.public_key):
    #         self.wallet.balance -= transaction.amount

    #     # check and update all peers
    #     for peer in self.peers:
    #         if peer.public_key == transaction.sender_address:
    #             peer.balance -= transaction.amount
    #         if peer.public_key == transaction.receiver_address:
    #             peer.balance += transaction.amount

    #     self.curr_block.add_transaction(transaction)
    #     self.q_transactions.append(transaction)

    #     if self.curr_block.is_full():
    #         print("Block is full, attempting minting...")
    #         # Current block is full, initiate mining process
    #         # call mine competition??
    #         self.proof_of_stake()
    #         # if that is successful then empty the queued transactions
    #         self.q_transactions.clear()
    #         self.curr_block = None
    #     else:
    #         print(f"Transaction of {transaction.amount} is added to queue block, capacity not reached.")

    #     return True