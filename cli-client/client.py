import sys
import cmd
sys.path.append('../')
from backend.node import Node

# TODO low priority magic to point to the right thing, 
node = Node()

class CLI:
    def __init__(self):
        self.balance = 0
        self.command_descriptions = {
            "m <recipient_address> <message>": "Send a message to a recipient",
            "stake <amount>": "Commit your stake of a specified amount",
            "view": "View the last validated block's transactions and the id of the validator.",
            "balance": "Check your balance",
            "help": "Show available commands and their descriptions"
            "t: <amount>: Create a new transaction transfering amount BCC"
        }
        self.commands = {
            "m": self.send_message,
            "stake": self.stake_amount,
            "view": self.view,
            "balance": self.check_balance,
            "help": self.show_help,
            "t": self.amount
        }

    def amount(self, args):
        if len(args) < 2:
            print("Error: 't' command requires both recipient address and message.")
            return
        recipient_address, amount = args
        #not sure if ammount is needed, added for clarity, gonna check it out #TODO (anast)
        # # TODO low prior call create transaction
        
        #  === Begin New transaction ===

        #Στείλε στο recipient_address wallet το ποσό amount από BTC coins που θα πάρει
        #από το wallet sender_address.
        #καλεί συνάρτηση create_transaction στο backend που θα
        #υλοποιεί την παραπάνω λειτουργία.
        #I'm sending to recipient amount BCC
        new_trans = self.create_transaction(self, recipient_address, "coins", amount, None ) #rest arguments ?? (Anast)
        
        # === End new Transaction ===
        
        print(f"Sending '{amount}' BCC to {recipient_address}")

    def send_message(self, args):
        if len(args) < 2:
            print("Error: 'm' command requires both recipient address and message.")
            return
        recipient_address, message = args
        # do i get charged for sending a message? Has this functionality been implemented? (Anast)
        #for now
        #TODO
        new_trans = self.create_transaction(self, recipient_address, "message", None, message ) #rest arguments ?? (Anast)

        print(f"Sending message '{message}' to {recipient_address}")

        pass


  
    def stake_amount(self, args):
        if len(args) < 1:
            print("Error: 'stake' command requires the amount to be specified.")
            return
        amount = args[0]

        
        # TODO low prior call stake() from backend, handle failure for insuff funds
        # I hope that is what u meant by insuff funds. If not #FIXME  (Anast)
        st = self.stake(amount)

        if not st:
            print("Not enough BCC in your account to bind...")
        else:
            print(f"Staking {amount}")


    def view(self, args):
        print("Viewing last validated block...\n\n")
        last_block = node.view_block()
        validator, transactions = last_block["validator"], last_block["transactions"]
        print(
            f"Validated by: {validator}\n\n"
            f"TRANSACTIONS\n"
            )
        for transaction in transactions:
            print(transaction)
            print("-" * 40)  


    def check_balance(self, args):
        # TODO low prior

        print(f"Your balance is: {self.balance}")

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

if __name__ == "__main__":
    cli = CLI()
    # anast added this by following instructions from https://medium.com/@noransaber685/simple-guide-to-creating-a-command-line-interface-cli-in-python-c2de7b8f5e05 
    cli.cmdloop()
    cli.start()

