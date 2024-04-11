import sys
sys.path.append('../')
import requests


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
            "t: <amount>": "Create a new transaction transferring amount BCC"
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
            print(print_colored("Error: 't' command requires both recipient address and amount.", "red"))
            return
        
        rec_id = args[0]
        amount = args[1]
        if rec_id is None:
            print(print_colored("Error: 'amount' requires a recipient address.", "red"))
            return
        if amount is None:
            print(print_colored("Error: 'amount' requires an amount.", "red"))
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
            print(print_colored(response_data['message'], "green"))
        elif response.status_code == 400:
            response_data = response.json()
            print(print_colored(response_data['message'], "red"))
        else:
            print(print_colored("Failed to create transaction. Error occurred.", "red"))



    def send_message2(self, args):
        # Check if rec_id or mess is None
        rec_id = args[0]
        mess = args[1]
        if len(args) > 2:
            for i in range(2, len(args)):
                mess = mess + " "+ args[i]
        if rec_id is None:
            print(print_colored("Error: 'send_message2' requires a recipient address.", "red"))
            return
        if mess is None:
            print(print_colored("Error: 'send_message2' requires a message.", "red"))
            return

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
            print(print_colored("Message sent successfully!", "green"))
        elif response.status_code == 400:
            print(print_colored("Failed to send message: Not enough NBCs.", "red"))
        else:
            print(print_colored("Failed to send message. Error occurred.", "red"))


    def stake_amount(self, args):
        # Get stake amount from user input or args
        amount = args[0]

        try:
            # Make a POST request to the /stake endpoint
            response = requests.post(f'http://{self.ip}:{self.port}/stake', json={"stake_amount": amount})

            # Check the response status code
            if response.status_code == 200:
                print(print_colored(response.json()['message'], "green"))  # Print success message
            elif response.status_code == 400:
                print(print_colored(response.json()['error'], "red"))  # Print error message
            else:
                print(print_colored(f"Error: {response.status_code}", "red"))
        
        except requests.exceptions.RequestException as e:
            print(print_colored(f"Error occurred: {e}", "red"))


    def view(self, args):
        try:
            # Make a GET request to the /view endpoint
            response = requests.get(f'http://{self.ip}:{self.port}/view')

            if response.status_code == 200:
                pass
  
            else:
                print(print_colored("Failed to retrieve data.", "red"))
        except Exception as e:
            print(print_colored(f"Error: {e}", "red"))


    def check_balance(self, args):
        # # TODO low prior
        # Construct the URL for the API endpoint
        url = f'http://{self.ip}:{self.port}/money'  # Update with your actual API URL
        #response = requests.post(f'http://{self.ip}:{self.port}/create_transaction', data=payload)

        # Send an HTTP GET request to the API endpoint
        response = requests.get(url)
        

        # Check the response status and handle accordingly
        if response.status_code == 200:
            # Assuming the response contains JSON data with 'balance' key
            balance = response.json().get('balance')
            print(print_colored(f"Your balance is: {balance}", "green"))
        else:
            print(print_colored("Failed to retrieve balance. Error occurred.", "red"))

        url = f'http://{self.ip}:{self.port}/pending_money'  # Update with your actual API URL
        #response = requests.post(f'http://{self.ip}:{self.port}/create_transaction', data=payload)

        # Send an HTTP GET request to the API endpoint
        response = requests.get(url)
        
        
        # Check the response status and handle accordingly
        if response.status_code == 200:
            # Assuming the response contains JSON data with 'balance' key
            balance = response.json().get('balance')
            print(print_colored(f"Your pending balance is: {balance}", "yellow"))
        else:
            print(print_colored("Failed to retrieve balance. Error occurred.", "red"))



    def show_help(self, args):
        max_command_length = max(len(command) for command in self.command_descriptions.keys())
        print(print_colored("\nAvailable commands:\n", "bold"))
        for command, description in self.command_descriptions.items():
            padding = ' ' * (max_command_length - len(command) + 4)
            print(f"{print_colored(command, 'cyan')}{padding}{description}")

    def run_command(self, command, args):
        if command in self.commands:
            self.commands[command](args)
        else:
            print(print_colored("Command not found. Type 'help' to see available commands.", "red"))

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
            try:
                user_input = input(print_colored("\n$ ", "cyan")).split()
                if not user_input:
                    continue
                command = user_input[0]
                args = user_input[1:]
                self.run_command(command, args)
            except KeyboardInterrupt:
                print(print_colored("\nExiting...", "red"))
                sys.exit(0)

# if __name__ == "__main__":
#     print("hi")
#     cli = CLI()
#     cli.start()
