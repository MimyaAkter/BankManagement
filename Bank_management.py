import os

filename = "bank_accounts.txt"
transaction_file = "transactions.txt"


def register():
    print("\n--- Register New Account ---")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    
    if os.path.exists(filename):
        f = open(filename, "r")
        for line in f:
            user, _, _ = line.strip().split(",")
            if user == username:
                print("Username already exists!")
                f.close()
                return
        f.close()
    
    balance = 0 
    f = open(filename, "a")
    f.write(f"{username},{password},{balance}\n")
    f.close()
    print("Account created successfully!")


def login():
    print("\n--- Login ---")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    
    if os.path.exists(filename):
        f = open(filename, "r")
        for line in f:
            user, pwd, balance = line.strip().split(",")
            if user == username and pwd == password:
                f.close()
                print("Login successful!")
                return username, int(balance)
        f.close()
    print("Invalid username or password!")
    return None, None


def deposit(username, current_balance):
    print("\n--- Deposit Money ---")
    amount = int(input("Enter amount to deposit: "))
    if amount > 0:
        current_balance += amount
        update_balance(username, current_balance)
        log_transaction(username, f"Deposited {amount}")
        print(f"Successfully deposited {amount}. Current Balance: {current_balance}")
    else:
        print("Invalid amount!")
    return current_balance


def withdraw(username, current_balance):
    print("\n--- Withdraw Money ---")
    amount = int(input("Enter amount to withdraw: "))
    if amount > 0 and amount <= current_balance:
        current_balance -= amount
        update_balance(username, current_balance)
        log_transaction(username, f"Withdrew {amount}")
        print(f"Successfully withdrew {amount}. Current Balance: {current_balance}")
    else:
        print("Invalid amount or insufficient balance!")
    return current_balance

def transfer(username, current_balance):
    print("\n--- Transfer Money ---")
    recipient = input("Enter recipient's username: ")
    amount = int(input("Enter amount to transfer: "))
    
    if amount > 0 and amount <= current_balance:
        if os.path.exists(filename):
            f = open(filename, "r")
            users = f.readlines()
            f.close()
            
            updated = False
            f = open(filename, "w")
            for line in users:
                user, pwd, balance = line.strip().split(",")
                if user == recipient:
                    new_balance = int(balance) + amount
                    f.write(f"{user},{pwd},{new_balance}\n")
                    updated = True
                elif user == username:
                    f.write(f"{user},{pwd},{current_balance - amount}\n")
                else:
                    f.write(line)
            f.close()
            
            if updated:
                log_transaction(username, f"Transferred {amount} to {recipient}")
                log_transaction(recipient, f"Received {amount} from {username}")
                print(f"Successfully transferred {amount} to {recipient}.")
                return current_balance - amount
            else:
                print("Recipient not found!")
        else:
            print("No users found!")
    else:
        print("Invalid amount or insufficient balance!")
    return current_balance


def account_statement(username):
    print("\n--- Account Statement ---")
    if os.path.exists(filename):
        f = open(filename, "r")
        for line in f:
            user, _, balance = line.strip().split(",")
            if user == username:
                print(f"Username: {username}, Balance: {balance}")
                print("\n--- Transaction History ---")
                display_transaction_history(username)
                break
        f.close()
    else:
        print("No account data found!")


def update_balance(username, new_balance):
    if os.path.exists(filename):
        f = open(filename, "r")
        users = f.readlines()
        f.close()
        
        f = open(filename, "w")
        for line in users:
            user, pwd, balance = line.strip().split(",")
            if user == username:
                f.write(f"{user},{pwd},{new_balance}\n")
            else:
                f.write(line)
        f.close()


def log_transaction(username, transaction):
    with open(transaction_file, "a") as f:
        f.write(f"{username},{transaction}\n")

def display_transaction_history(username):
    if os.path.exists(transaction_file):
        with open(transaction_file, "r") as f:
            transactions = [line.strip().split(",")[1] for line in f if line.startswith(username)]
        if transactions:
            for transaction in transactions:
                print(transaction)
        else:
            print("No transactions found!")
    else:
        print("No transaction history available.")


def user_menu(username, balance):
    while True:
        print("\n--- Bank Menu ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Transfer Money")
        print("4. Account Statement")
        print("5. Transaction History")  
        print("6. Logout")
        choice = input("Choose an option: ")
        
        if choice == "1":
            balance = deposit(username, balance)
        elif choice == "2":
            balance = withdraw(username, balance)
        elif choice == "3":
            balance = transfer(username, balance)
        elif choice == "4":
            account_statement(username)
        elif choice == "5": 
            print("\n--- Transaction History ---")
            display_transaction_history(username)
        elif choice == "6":
            print("Logged out successfully!")
            break
        else:
            print("Invalid choice, try again!")


def main():
    while True:
        print("\n--- Bank Account Management ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            username, balance = login()
            if username:
                user_menu(username, balance)
        elif choice == "3":
            print("Thank you for using the Bank System. Goodbye!")
            break
        else:
            print("Invalid choice, try again!")


main()