from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from tabulate import tabulate
from blockchain import Blockchain ##to prosuesa egw ATHINA




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

    def __init__(self, sender_address, receiver_address, type_of_transaction, amount, message, noance):#αφαιρεσα το signature ως attribute και εβαλα το noance γτ το αρχικοποιουμε στο node.py
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        
        if (type_of_transaction == "message"):
            self.message = message
            self.amount = len(message) #seems ok

        else:
            self.message = None
            self.amount = amount
            
        self.nonce = noance  #το εκανα προσφατα modify (αθηνά) οταν ερθει η
                             #ωρα να προσθεσουμε ενα transaction στο μπλοκ τσεκαρουμε 
                             #αν το ζευγος sender_address,noance υπαρχει ηδη στο  nonce_history του Blockchain

        

        # self.transaction_id # TODO

    #  self.transaction_id = id if id is not None else self.calculate_transaction_id() συνφωνω με αυτον τον κωδικα αθ τον τσεκαρω κ εγω ξανα (αθηνα)

    # def calculate_transaction_id(self):
    #     """
    #     Calculates the hash of the transaction using SHA-256 algorithm.
    #     """
    #     if self.message is None:
    #         tx_content = f"{self.sender_address}{self.receiver_address}{self.type_of_transaction}{self.amount}{self.nonce}".encode()
    #     else:
    #         tx_content = f"{self.sender_address}{self.receiver_address}{self.type_of_transaction}{self.message}{self.nonce}".encode()
    #     return hashlib.sha256(tx_content).hexdigest()
        
        self.signature = None


    # made this to print in view command, use by print(transaction object)
    def __str__(self):
        if self.type_of_transaction == "message":
            transaction_type = "Message"
            details = f"Message: {self.message}"
        else:
            transaction_type = "Transfer"
            details = f"Amount: {self.amount}"

        transaction_data = [
            ["Transaction Type", transaction_type],
            ["Sender Address", self.sender_address],
            ["Receiver Address", self.receiver_address],
            [f"{transaction_type} Details", details],
            ["Signature", self.signature.hex() if self.signature else 'Not signed yet']
        ]

        return tabulate(transaction_data, tablefmt="fancy_grid")

    def sign_transaction(self, private_key):
        
        serialized_private_key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
        )

        message = self._get_message_to_sign()
        self.signature = serialized_private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )

    def verify_signature(self):
        
        sender_public_key = serialization.load_pem_public_key(
            self.sender_address.encode(),
            backend=default_backend()
        )

        message = self._get_message_to_sign()
        try:
            sender_public_key.verify(
                self.signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                utils.Prehashed(hashes.SHA256())
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False

    def _get_message_to_sign(self):
        if self.type_of_transaction == "message":
            return self.message.encode()
        else:
            return str(self.amount).encode()


