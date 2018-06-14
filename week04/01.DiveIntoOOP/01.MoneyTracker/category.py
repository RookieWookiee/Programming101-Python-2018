from abc import ABC, abstractmethod

class Category(ABC):
    @abstractmethod
    def __str__(self):
        pass

class Expense(Category):
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category
        self._type = 'Expense'
