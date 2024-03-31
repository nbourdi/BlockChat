from Crypto.PublicKey import RSA

class Wallet:

    def generate_wallet(self):
        # Generate RSA key pair
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        self.private_key = private_key.export_key(format='PEM').decode()
        self.public_key = public_key.export_key(format='PEM').decode()
        
    def init(self):
        self.generate_wallet()
        self.balance = 0 # i added that, balance = blockchat coins