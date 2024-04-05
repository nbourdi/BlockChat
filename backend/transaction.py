import base64
import hashlib
import logging
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from tabulate import tabulate

# Κάθε transaction περιέχει πληροφορίες για την αποστολή νομισμάτων/μηνύματος από ένα wallet
# σε ένα άλλο. Οι πληροφορίες που περιλαμβάνει είναι
# sender_address: To public key του wallet από το οποίο προέρχεται το μήνυμα
# receiver_address: To public key του wallet παραλήπτη του μηνύματος
# type_of_transaction: Καθορίζει τον τύπο του transaction (coins or message)
# amount: το ποσο νομισμάτων προς αποστολή
# message: το String του μηνύματος που στέλνεται
# nonce: counter που διατηρείται ανά αποστολέα και αυξάνεται κατά 1 μετά από κάθε αποστολή
# transaction_id: το hash του transaction
# Signature: Υπογραφή που αποδεικνύει ότι ο κάτοχος του wallet δημιούργησε αυτό το transaction

class Transaction:

    def __init__(self, sender_address, receiver_address, type_of_transaction, amount, message,nonce,transaction_id=None, signature=None):#αφαιρεσα το signature ως attribute και εβαλα το nonce γτ το αρχικοποιουμε στο node.py
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        # self.signature = None  # Initialize signature attribute
        
        if (type_of_transaction == "message"):
            self.message = message
            self.amount = len(message) #seems ok

        else:
            self.message = None
            self.amount = amount
            
        self.nonce = nonce  #το εκανα προσφατα modify (αθηνά) οταν ερθει η
                             #ωρα να προσθεσουμε ενα transaction στο μπλοκ τσεκαρουμε 
                             #αν το ζευγος sender_address,noance υπαρχει ηδη στο  nonce_history του Blockchain

        self.transaction_id = transaction_id if transaction_id else self.calculate_transaction_id() 
        self.signature = signature if signature else None
 

##ΤΟ ΕΒΓΑΛΑ ΑΠΟ ΤΑ ΣΧΟΛΙΑ ΠΟΥ ΥΠΗΡΧΕ ΓΤ Μ ΦΑΝΗΚΕ ΚΟΜΠΛΕ
    def calculate_transaction_id(self):
        
        if self.message is None:
            tx_content = f"{self.sender_address}{self.receiver_address}{self.type_of_transaction}{self.amount}{self.nonce}".encode()
        else:
            tx_content = f"{self.sender_address}{self.receiver_address}{self.type_of_transaction}{self.message}{self.nonce}".encode()
        return hashlib.sha256(tx_content).hexdigest()
        


    # made this to print in view command, use by print(transaction object)
    def __str__(self):
        if self.type_of_transaction == "message":
            transaction_type = "Message"
            details = f"Message: {self.message}"
        else:
            transaction_type = "Transfer"
            details = f"Amount: {self.amount}"

        signature_status = 'Not signed yet' if self.signature is None else 'Signed'

        transaction_str = f"Transaction Type: {transaction_type}\n"
        transaction_str += f"Sender Address: {self.sender_address}\n"
        transaction_str += f"Receiver Address: {self.receiver_address}\n"
        transaction_str += f"{transaction_type} Details: {details}\n"
        transaction_str += f"Signature: {signature_status}"

        return transaction_str

    # def sign_transaction(self, private_key):
    #     private_key = RSA.import_key(private_key)
    #     message = self._get_message_to_sign()
    #     h = SHA256.new(message)
    #     self.signature = pkcs1_15.new(private_key).sign(h)

    # def verify_signature(self):
    #     print("HI MY SIGNATURE IS THIS in verify sig")
    #     print(self.signature)
    #     sender_public_key = RSA.import_key(self.sender_address)
    #     message = self._get_message_to_sign()
    #     h = SHA256.new(message)
    #     try:
    #         pkcs1_15.new(sender_public_key).verify(h, self.signature)
    #         return True
    #     except (ValueError, TypeError):
    #         print("Signature verification failed")
    #         return False

    def sign_transaction(self, private_key):
        private_key = RSA.import_key(private_key)
        message = self._get_message_to_sign()
        h = SHA256.new(message)
        self.signature = pkcs1_15.new(private_key).sign(h)
        print("Signed message: %s", self.signature.hex())  # Log the signed message

    def verify_signature(self):
        sender_public_key = RSA.import_key(self.sender_address)
        message = self._get_message_to_sign()
        h = SHA256.new(message)
        try:
            pkcs1_15.new(sender_public_key).verify(h, self.signature)
            print("Signature verified successfully")
            return True
        except (ValueError, TypeError):
            print("Signature verification failed")
            return False


    def _get_message_to_sign(self):
        if self.type_of_transaction == "message":
            return self.message.encode()
        else:
            return str(self.amount).encode()
        

    def to_dict(self):
        transaction_dict = {
            'sender_address': self.sender_address,
            'receiver_address': self.receiver_address,
            'type_of_transaction': self.type_of_transaction,
            'amount': self.amount,
            'nonce': self.nonce,
            'message': self.message,
            'transaction_id': self.transaction_id,
            'signature': self.signature
        }
        return transaction_dict

    # def from_dict(cls, transaction_dict):
    #     return cls(
    #         sender_address=transaction_dict['sender_address'],
    #         receiver_address=transaction_dict['receiver_address'],
    #         type_of_transaction=transaction_dict['type_of_transaction'],
    #         amount=transaction_dict['amount'],
    #         nonce=transaction_dict['nonce'],
    #         message=transaction_dict['message'],
    #         transaction_id=transaction_dict['transaction_id'],
    #         signature=transaction_dict['signature']
    #     )

    def from_dict(cls, transaction_dict):
    # Decode base64 signature to byte string
        if transaction_dict['signature']:
            transaction_dict['signature'] = base64.b64decode(transaction_dict['signature'])
        
        return cls(
            sender_address=transaction_dict['sender_address'],
            receiver_address=transaction_dict['receiver_address'],
            type_of_transaction=transaction_dict['type_of_transaction'],
            amount=transaction_dict['amount'],
            nonce=transaction_dict['nonce'],
            message=transaction_dict['message'],
            transaction_id=transaction_dict['transaction_id'],
            signature=transaction_dict['signature']
    )
    
    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

