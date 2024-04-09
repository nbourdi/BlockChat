# from node import node
import sys
sys.path.append('../')
import requests

# from backend.node import Node
# from node import Node

# TODO low priority magic to point to the right thing, 
#node = Node()


def print_header(text):
    print(f"\n{'='*30} {text} {'='*30}")

def print_block_details(last_block):
    print_header("Last Block Details")
    print(f"Validator: {last_block['validator']}")

def print_transactions(transactions):
    print_header("Transactions")
    for transaction in transactions:
        print(f"Transaction ID: {transaction['id']}")
        print(f"Sender: {transaction['sender']}")
        print(f"Recipient: {transaction['recipient']}")
        print(f"Amount: {transaction['amount']}")
        if 'message' in transaction:
            print(f"Message: {transaction['message']}")
        print("-" * 50)


def print_colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    color_code = colors.get(color.lower(), '')
    return f"{color_code}{text}{colors['end']}"

def print_box(text, color):
    length = len(text) + 4
    print(print_colored('╔' + '═' * length + '╗', color))
    print(print_colored('║ ' + text + ' ║', color))
    print(print_colored('╚' + '═' * length + '╝', color))


class CLI:
    def __init__(self, ip, port):
        self.balance = 0
        self.command_descriptions = {
            "m <recipient_address> <message>": "Send a message to a recipient",
            "stake <amount>": "Commit your stake of a specified amount",
            "view": "View the last validated block's transactions and the id of the validator.",
            "balance": "Check your balance",
            "help": "Show available commands and their descriptions", 
            "t <amount>": "Create a new transaction transfering amount BCC"
        }
        self.commands = {
            "m": self.send_message2,
            "stake": self.stake_amount,
            "view": self.view,
            "balance": self.check_balance,
            "help": self.show_help,
            "t": self.amount
        }
        self.ip = ip
        self.port = port

    
    def amount(self, args):
        if len(args) < 2:
            print("Error: 't' command requires both recipient address and amount.")
            return
        
        rec_id = args[0]
        amount = args[1]
        if rec_id is None:
            print("Error: 'amount' requires a recipient address.")
            return
        if amount is None:
            print("Error: 'amount' requires a message.")
            return
        # Prepare the payload for the HTTP POST request
        payload = {
            'receiver': rec_id,
            'type': 'coins',  # Assuming type of transaction is 'coins' for sending amount
            'amount': amount  # The amount to send
        }
        
        url = f'http://{self.ip}:{self.port}/create_transaction'
        # Send an HTTP POST request to the create_transaction endpoint
        response = requests.post(url, data=payload)
        
        # Check the response status and handle accordingly
        if response.status_code == 200:
            response_data = response.json()
            print(response_data['message'])
           # print(f"Current Balance: {response_data['balance']}")
        elif response.status_code == 400:
            response_data = response.json()
            print(response_data['message'])
           # print(f"Current Balance: {response_data['balance']}")
        else:
            print("Failed to create transaction. Error occurred.")




   
   



    def send_message2(self, args):
        # Check if rec_id or mess is None
        print( "lenght od args = " ,len(args))
        rec_id = args[0]
        mess = args[1]
        if len(args):
            for i in range(2, len(args)):
                mess = mess + " "+ args[i]
        if rec_id is None:
            print("Error: 'send_message2' requires a recipient address.")
            return
        if mess is None:
            print("Error: 'send_message2' requires a message.")
            return

        # Print recipient ID and message for debugging
        print("Recipient ID:", rec_id)
        print("Message:", mess)

        # Prepare the payload for the HTTP POST request
        payload = {
            'receiver': rec_id,
            'type': 'message',
            'message': mess
        }

        # Make the HTTP POST request to your endpoint
        response = requests.post(f'http://{self.ip}:{self.port}/create_transaction', data=payload)

        # Check the response status and handle accordingly
        if response.status_code == 200:
            print("Message sent successfully!")
        elif response.status_code == 400:
            print("Failed to send message: Not enough NBCs.")
        else:
            print("Failed to send message. Error occurred.")






    def stake_amount(self, args):
        # Get stake amount from user input or args
        amount = args[0]

        try:
            # Make a POST request to the /stake endpoint
            response = requests.post(f'http://{self.ip}:{self.port}/stake', json={"stake_amount": amount})

            # Check the response status code
            if response.status_code == 200:
                print(response.json()['message'])  # Print success message
            elif response.status_code == 400:
                print(response.json()['error'])  # Print error message
            else:
                print(f"Error: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")



    def view(self, args):
        try:
            # Make a GET request to the /view endpoint
            response = requests.get(f'http://{self.ip}:{self.port}/view')

            # Check the response status code
            if response.status_code == 200:
                last_block = response.json()
                print_block_details(last_block)

                if last_block['transactions']:
                    transactions = last_block['transactions']
                    print_transactions(transactions)
                else:
                    print("\nNo transactions available in this block.")

            elif response.status_code == 404:
                print("\nNo blocks available")

            else:
                print(f"\nError: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"\nError occurred: {e}")


    def check_balance(self, args):
        # # TODO low prior
        # print(f"Your balance is: {self.balance}")
        # Construct the URL for the API endpoint
        url = f'http://{self.ip}:{self.port}/money'  # Update with your actual API URL
        #response = requests.post(f'http://{self.ip}:{self.port}/create_transaction', data=payload)

        # Send an HTTP GET request to the API endpoint
        response = requests.get(url)
        
        # Check the response status and handle accordingly
        if response.status_code == 200:
            # Assuming the response contains JSON data with 'balance' key
            balance = response.json().get('balance')
            print(f"Your balance is: {balance}")
        else:
            print("Failed to retrieve balance. Error occurred.")



    def show_help(self, args):
        max_command_length = max(len(command) for command in self.command_descriptions.keys())
        print("\n\033[1mAvailable commands:\033[0m\n")
        for command, description in self.command_descriptions.items():
            padding = ' ' * (max_command_length - len(command) + 4)
            print(f"\033[93m{command}\033[0m{padding}{description}")

    def run_command(self, command, args):
        if command in self.commands:
            self.commands[command](args)
        else:
            print("Command not found. Type 'help' to see available commands.")

    def welcome_message(self):
        print("""
              

██████╗ ██╗      ██████╗  ██████╗██╗  ██╗ ██████╗██╗  ██╗ █████╗ ████████╗    
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██║  ██║██╔══██╗╚══██╔══╝    
██████╔╝██║     ██║   ██║██║     █████╔╝ ██║     ███████║███████║   ██║       
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██║     ██╔══██║██╔══██║   ██║       
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗╚██████╗██║  ██║██║  ██║   ██║       
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  


To get started, type 'help' to see available commands.
        """)

    def start(self):
        self.welcome_message()
        while True:
            user_input = input("\n93m$ ").split()
            if not user_input:
                continue
            command = user_input[0]
            args = user_input[1:]
            self.run_command(command, args)
