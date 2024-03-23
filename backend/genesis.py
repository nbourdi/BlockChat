ip = '127.0.0.1' # localhost
port = 3000 

# stake = 
# capacity = 
from node import Node
def main():
    # Create an instance of the Node class
    node1 = Node(capacity=5, stake=10)

    # Test some functionality of the Node class]
    node1.id=1
    print("Node ID:", node.id)
    print("Node Wallet Public Key:", node.wallet.public_key)
    print("Node Blockchain Length:", len(node.blockchain.blocks))
    # You can continue testing other methods and attributes of the Node class here

# Entry point of the script
if __name__ == "__main__":
    main()
