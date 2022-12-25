import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InSufficientFunds

@pytest.mark.parametrize("num1, num2, expected", [      ##parameterize
    (4, 5, 9),
    (10, 5, 15),
    (9, 4, 13)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(5, 4) == 1


def test_multiply():
    assert multiply(4, 5) == 20


def test_divide():
    assert divide(20, 5) == 4


@pytest.fixture
def zero_bank_account():
    return BankAccount()

"""
#Testing classes

def test_bank_initial_amount():
    bank_ac = BankAccount(50)
    assert bank_ac.balance == 50


def test_bank_default_amount():
    bank_ac = BankAccount()
    assert bank_ac.balance == 0


def test_bank_withdraw():
    bank_ac = BankAccount(100)
    bank_ac.withdraw(25)
    assert bank_ac.balance == 75


def test_bank_deposit():
    bank_ac = BankAccount(150)
    bank_ac.deposit(50)
    assert bank_ac.balance == 200


def test_bank_collect_interest():
    bank_ac = BankAccount(100)
    bank_ac.collect_interest()
    assert round(bank_ac.balance) == 110    # 100*1.1 = 110.00000000000001
"""

## Testing class with fixtures

@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40


def test_bank_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55    # 100*1.1 = 110.00000000000001


# Fixture and parameterize
@pytest.mark.parametrize("deposited, withdrew, expected", [      ##parameterize
    (100, 25, 75),
    (200, 50, 150),
    (620, 120, 500)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InSufficientFunds):
        bank_account.withdraw(200)      #available bal = 100; but, with drawing 200 rupees