class Blockchain:

    def __init__(self):
        self.blocks = [] # just a list of all the blocks that are currently validated
        # nonce epifulaksi
        self.nonce_history = {}  # Ένα λεξικό που θα κρατάει το ιστορικό των nonces ανάλογα με τον λογαριασμό

    def add_block(self, block):
        self.blocks.append(block)


# Για την πρόληψη επιθέσεων επανάληψης (replay attacks), όπου κάποιος κακόβουλος κόμβος θα
# μπορούσε να ξαναστείλει ένα transaction που έλαβε για να χρεώσει ξανά τον αποστολέα, κάθε
# συναλλαγή στο μοντέλο λογαριασμού περιέχει ένα πεδίο nonce. Το nonce είναι ένας μετρητής που
# διατηρεί κάθε λογαριασμός στο BlockChat και που αυξάνεται κατά ένα με κάθε εξερχόμενη
# συναλλαγή. Αυτό εμποδίζει την υποβολή της ίδιας συναλλαγής περισσότερες από μία φορές στο
# δίκτυο.

# TODO erwtisi: auto mipws einai gia to transaction class? to blockchain einai mono 1 opote de xreiazetai nonce (nat)
    def add_nonce(self, account_address, nonce):
        if account_address not in self.nonce_history:
            self.nonce_history[account_address] = set()
        self.nonce_history[account_address].add(nonce)    

    def is_nonce_used(self, account_address, nonce):
        return nonce in self.nonce_history.get(account_address, set())


    # TODO needed gia to broadcast tou chain, 
    # to afhnw gia otan eimaste sigoures gia ta pedia tou chain (nat)
    def to_dict():
        pass
    def from_dict():
        pass
