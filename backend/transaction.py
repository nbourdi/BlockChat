from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from tabulate import tabulate

class Transaction:

    def __init__(self, sender_address, receiver_address, type_of_transaction, amount, message, signature):
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        
        if (type_of_transaction == "message"):
            self.message = message
            # self.amount = len(message) # TODO , need to be calculated here

        else:
            self.message = None
            self.amount = amount
            
        self.nonce = None  # TODO
        # self.transaction_id # TODO
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


