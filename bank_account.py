class Account:
    def __init__(self, acc_num, type, name, bal=0):
        """
        Creates a bank account. If no balance is specified defaults to
        zero.
        :param acc_num: string
        :param type: string
        :param name: string
        :param bal: int/float
        """
        if not isinstance((name or type or acc_num), str):
            raise TypeError("Account name/type/number is not string.")
        self.acc_num = acc_num
        self.type = type
        self.name = name
        self.bal = bal

    def deposit(self, value):
        """
        Deposits an amount into the account.
        If the value is less than 0 raise ValueError
        If the value is not a number raise TypeError
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Deposit amount must be a number")
        if value < 0:
            raise ValueError("Can't deposit a negative amount")
        self.bal += value

    def withdraw(self, value):
        """
        Withdraws an amount into the account.
        If the value is less than 0 raise ValueError
        If the value is not a number raise TypeError
        If the withdrawn amount exceeds the balance notify the user.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Withdrawn amount must be a number")
        if value < 0:
            raise ValueError("Can't withdraw a negative amount")
        if value > self.bal:
            return (f"withdrawal amount {value} exceeds the balance "
                    f"of {self.bal} for {self.name} account.")
        self.bal -= value

    def __str__(self):
        return (f"account_number: {self.acc_num}, type: {self.type},"
                f" account_name: {self.name}, balance: {self.bal}")


class AccountDataBase:
    """
    Represents the database of bank accounts.
    """
    def __init__(self):
        """
        Creates the database. The database is PRIVATE.
        """
        self.__account_database = []

    @property
    def account_database(self):
        """
        Getter for the database.
        """
        return self.__account_database

    def insert(self, user_data):
        """
        Inserts a user into the database if user_data doesn't exist
        in the database.
        """
        index = self.__search(user_data.acc_num)
        if index == -1:
            self.account_database.append(user_data)

    def __search(self, acc_num):
        """
        Internal search function to find an account.
        """
        for i in range(len(self.account_database)):
            if acc_num == self.account_database[i].acc_num:
                return i
        return -1

    def search(self, acc_num):
        """
        Public search function.
        """
        for i in range(len(self.account_database)):
            if acc_num == self.account_database[i].acc_num:
                return self.account_database[i]
        return

    def delete(self, acc_num):
        """
        Deletes specified account. If no account is detected raise ValueError.
        """
        if self.__search(acc_num) == -1:
            raise ValueError("invalid account number; nothing to be deleted.")
        self.account_database.pop(self.__search(acc_num))

    def __str__(self):
        string = ""
        for i in self.__account_database:
            string += str(i) + "\n"
        return string


# Test case for delete.
a = Account("0000", "saving", "David Patterson", 1000)
b = Account("0001", "checking", "John Hennessy", 2000)
c = Account("0003", "saving", "Mark Hill", 3000)
d = Account("0004", "saving", "David Wood", 4000)
e = Account("0004", "saving", "David Wood", 4000)
data = AccountDataBase()
data.insert(a)
data.insert(b)
data.insert(c)
data.insert(d)
data.insert(e)
print(data)
data.delete("0000")
print(data)
