from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Wallet:
    def generate_wallet(self):
        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()

        self.private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        self.public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def __init__(self):
        self.generate_wallet()
        self.balance = 0 # i added that, balance = blockchat coins



# IF IT IS NOT WORKING REPLACE THE CODE WITH THIS 
# from Crypto.PublicKey import RSA

# class Wallet:
#     def generate_wallet(self):
#             # Generate RSA key pair
#             private_key = RSA.generate(2048)

#             public_key = private_key.publickey()

#             self.private_key = private_key.export_key(format='PEM').decode()
#             self.public_key = public_key.export_key(format='PEM').decode()

#     def __init__(self):
#         self.generate_wallet()
#         self.balance = 0 # i added that, balance = blockchat coins












