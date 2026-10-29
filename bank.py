import json
import os

DATA_FILE = "bank_data.json"
accounts = {}


def load_data():
    """Load saved accounts from the JSON file."""
    global accounts

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                accounts = json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read saved data. Starting with empty data.")
            accounts = {}
    else:
        accounts = {}


def save_data():
    """Save account information to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


def create_account():
    name = input("Enter account holder name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    pin = input("Create a 4-digit practice PIN: ").strip()
    if not (pin.isdigit() and len(pin) == 4):
        print("PIN must contain exactly 4 digits.")
        return

    # Generate a simple unique account number.
    account_number = str(max([int(number) for number in accounts if number.isdigit()] or [10000]) + 1)

    accounts[account_number] = {
        "name": name,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }
    save_data()
    print("\nAccount created successfully!")
    print("Your account number is:", account_number)
    print("Remember your account number and PIN.")


def authenticate():
    account_number = input("Enter account number: ").strip()
    pin = input("Enter 4-digit PIN: ").strip()

    account = accounts.get(account_number)
    if account is None or account.get("pin") != pin:
        print("Invalid account number or PIN.")
        return None, None

    return account_number, account


def check_balance():
    _, account = authenticate()
    if account is not None:
        print(f"Current balance: ₹{account['balance']:.2f}")


def deposit_money():
    account_number, account = authenticate()
    if account is None:
        return

    try:
        amount = float(input("Enter deposit amount (₹): "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    account["balance"] = round(account["balance"] + amount, 2)
    account["transactions"].append({
        "type": "Deposit",
        "amount": round(amount, 2)
    })
    save_data()
    print(f"Deposit successful. New balance: ₹{account['balance']:.2f}")


def withdraw_money():
    account_number, account = authenticate()
    if account is None:
        return

    try:
        amount = float(input("Enter withdrawal amount (₹): "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > account["balance"]:
        print("Insufficient balance.")
        return

    account["balance"] = round(account["balance"] - amount, 2)
    account["transactions"].append({
        "type": "Withdrawal",
        "amount": round(amount, 2)
    })
    save_data()
    print(f"Withdrawal successful. New balance: ₹{account['balance']:.2f}")


def transfer_money():
    sender_number, sender = authenticate()
    if sender is None:
        return

    receiver_number = input("Enter receiver account number: ").strip()
    receiver = accounts.get(receiver_number)

    if receiver is None:
        print("Receiver account not found.")
        return

    if receiver_number == sender_number:
        print("You cannot transfer money to the same account.")
        return

    try:
        amount = float(input("Enter transfer amount (₹): "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > sender["balance"]:
        print("Insufficient balance.")
        return

    sender["balance"] = round(sender["balance"] - amount, 2)
    receiver["balance"] = round(receiver["balance"] + amount, 2)

    sender["transactions"].append({
        "type": f"Transfer to {receiver_number}",
        "amount": round(amount, 2)
    })
    receiver["transactions"].append({
        "type": f"Transfer from {sender_number}",
        "amount": round(amount, 2)
    })

    save_data()
    print("Transfer successful!")
    print(f"Your new balance: ₹{sender['balance']:.2f}")


def view_account_details():
    account_number, account = authenticate()
    if account is not None:
        print("\n--- Account Details ---")
        print("Account holder:", account["name"])
        print("Account number:", account_number)
        print(f"Balance: ₹{account['balance']:.2f}")


def view_transaction_history():
    _, account = authenticate()
    if account is None:
        return

    transactions = account.get("transactions", [])
    print("\n--- Transaction History ---")
    if not transactions:
        print("No transactions yet.")
        return

    for index, transaction in enumerate(transactions, start=1):
        print(
            f"{index}. {transaction['type']} - "
            f"₹{transaction['amount']:.2f}"
        )


def main():
    load_data()

    while True:
        print("\n" + "=" * 36)
        print("       WELCOME TO SUJAL'S BANK")
        print("=" * 36)
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. View Account Details")
        print("7. View Transaction History")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            check_balance()
        elif choice == "3":
            deposit_money()
        elif choice == "4":
            withdraw_money()
        elif choice == "5":
            transfer_money()
        elif choice == "6":
            view_account_details()
        elif choice == "7":
            view_transaction_history()
        elif choice == "0":
            print("Thank you for using My Bank. Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from 0 to 7.")


if __name__ == "__main__":
    main()
