from decimal import Decimal, InvalidOperation


class Account:
    def __init__(self, pin: str, balance: Decimal):
        self.pin = pin
        self.balance = balance

    def authenticate(self, entered_pin: str) -> bool:
        return entered_pin == self.pin

    def deposit(self, amount: Decimal) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        return True


def read_amount(prompt: str) -> Decimal | None:
    try:
        amount = Decimal(input(prompt).strip())
    except (InvalidOperation, EOFError):
        print("Invalid amount.")
        return None

    if amount.as_tuple().exponent < -2:
        print("Please enter an amount with no more than two decimal places.")
        return None
    return amount


def main() -> None:
    account = Account(pin="1234", balance=Decimal("100"))

    print("Welcome to the ATM")
    for attempt in range(3):
        if account.authenticate(input("Enter your PIN: ").strip()):
            break
        remaining = 2 - attempt
        if remaining >= 0:
            print(f"Incorrect PIN. {remaining} attempt(s) remaining.")
    else:
        print("Too many incorrect attempts.")
        return

    while True:
        print("\n1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"Balance: ${account.balance:.2f}")
        elif choice == "2":
            amount = read_amount("Deposit amount: $")
            if amount is not None and account.deposit(amount):
                print(f"Deposited ${amount:.2f}")
            elif amount is not None:
                print("Deposit amount must be greater than zero.")
        elif choice == "3":
            amount = read_amount("Withdrawal amount: $")
            if amount is not None and account.withdraw(amount):
                print(f"Withdrew ${amount:.2f}")
            elif amount is not None:
                print("Insufficient balance or invalid withdrawal amount.")
        elif choice == "4":
            print("Thank you for using the ATM.")
            break
        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main()