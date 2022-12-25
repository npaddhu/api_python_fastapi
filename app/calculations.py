
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2    


class InSufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, starting_balance=0) -> None:
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InSufficientFunds("Insufficient funds in account")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance = self.balance * 1.1
        