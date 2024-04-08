from Crypto.PublicKey import RSA

class Wallet:

    def __init__(self):
        # Generate RSA key pair
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        self.private_key = private_key.export_key(format='PEM').decode()
        self.public_key = public_key.export_key(format='PEM').decode()
        self.balance = 0  
