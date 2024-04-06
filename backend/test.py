import json
from transaction import Transaction
from block import Block
from blockchain import Blockchain


#data = {'blocks': [{'index': 0, 'validator': 0, 'capacity': 2,'timestamp': 1712263889.0811503, 'transactions': [{'sender_address': '0', 'receiver_address': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1dPtaiqu6gMx8xTKoh4A\n9cUKkqtcnC0PkcTog38WI/EUvnNNRYMKBuJRgK5Dhr3At+i4s6ArUO2kNsjRateR\nxtXShUYRNotfGbKXoEvCbhdrgcnawzQrlnUGVLOgel1qlQyPONH2R0SEhDuylYra\nlMTOmUAfayao2BeFbnvXhXmxN6faAu6qN6GWPUZWCMkoNt6sgGS/wTT+BWIoAKcR\nIi9PTerjTnTtuLAeZoM18XIYIxeqnq5GDT3NYINVVZBtTG5AkgVk7LRrl+SRceAR\n+/xeWhEwkp4pca7gcdjpgBHsqI7wWQfJcSTqvNuSxi4gmRwZswGIe5PPByGzb/AO\nhwIDAQAB\n-----END PUBLIC KEY-----', 'type_of_transaction': 'coins', 'amount': 5000, 'nonce': 0, 'message': None, 'transaction_id': 'aa920cbf5e7eefc2821b27b425abadc08946d794e7340121934b8d02cf0650df', 'signature': None}], 'previous_hash': 1, 'nonce': None}]}
# data = {'blocks': [{'index': 0, 'current_hash': '222', 'timestamp': 1712408257.285173, 'transactions': [{'sender_address': '0', 'receiver_address': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs3rhq/K9gGvSSB9Saywy\nXTSkqS2z7k6vgBkz91tG7xW7qnzJtIWpUDyXC+GExPc7qtgQIdmdkxEOi0YZGAkZ\nKCZ+tWnSS+vRcHjKGyhGeejQ2TgAyLRCIUYWgPbqJucmo8nTLU5VPTZDEex0qiP2\nTNOVQYh0pqpmcyXxNhh219KemviK8dwiBrpnujvuPlkUU/C1ZQ7zF4+EMxhz+B30\n9FPWkF9RoNWQUlJu4svLmWW1zmJ8jHrfcEruYlHlo07nDJQWrSirUTCXxdDu+mQ4\nik+JzJ82nBUsaa/TaJngEIGGl5CwqHr7QsGYaScRyTYdDltRv/HpODhForsueVA3\n+wIDAQAB\n-----END PUBLIC KEY-----', 'type_of_transaction': 'coins', 'amount': 5000, 'nonce': 0, 'message': None, 'transaction_id': '9f462ecb088b6ae348e33ab2edbeebb226b751c71863d476843eacae520bc57c', 'signature': None}], 'previous_hash': 1, 'nonce': None, 'capacity': 1, 'validator': 0}]}
# chain = Blockchain.from_json(data)

# print(chain.blocks[-1].transactions[-1].receiver_address)

block = Block(index=6, previous_hash=6, validator=0, capacity=1, current_hash=0)

tran = Transaction(sender_address=0, receiver_address=0, amount=0, type_of_transaction="coins", transaction_id=1, message=None, signature=0, nonce=1)
block.add_transaction(tran)
block_json = block.to_dict()
block_json = json.dumps(block.to_dict())
print(block_json)