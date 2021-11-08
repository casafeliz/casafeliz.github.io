class CEO:
    __shared_state = {
        "name": "Bob",
        "age": 55
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return f"{self.name} is {self.age} years old"


def test_ceo():
    ceo1 = CEO()
    assert str(ceo1) == "Bob is 55 years old"
    ceo2 = CEO()
    ceo2.age = 77
    assert str(ceo1) == "Bob is 77 years old"
    assert str(ceo2) == "Bob is 77 years old"


class Monostate:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Monostate, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj


class CFO(Monostate):
    def __init__(self):
        self.name = ""
        self.money_managed = 0

    def __str__(self):
        return f"{self.name} manages ${self.money_managed}"


def test_cfo():
    cfo1 = CFO()
    cfo1.name = "Jack"
    cfo1.money_managed = 1
    assert str(cfo1) == "Jack manages $1"
    cfo2 = CFO()
    cfo2.name = "Mac"
    cfo2.money_managed = 10
    assert str(cfo1) == "Mac manages $10"
    assert str(cfo2) == "Mac manages $10"
