from abc import ABC, abstractmethod


class Calculation(ABC):

    def __init__(self, a, b, operation):
        # self refers to this particular calculation.
        self.a = a
        self.b = b
        self.operation = operation

    @classmethod
    def create(cls, a, b, operation):
        # cls is the concrete class calling this factory.
        return cls(a, b, operation)

    @abstractmethod
    def execute(self):
        # Abstract placeholder; subclasses provide the behavior.
        pass  # pragma: no cover


class ArithmeticCalculation(Calculation):

    def execute(self):
        # Instance methods can use the object's stored values.
        return self.operation(self.a, self.b)