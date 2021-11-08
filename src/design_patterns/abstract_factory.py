from abc import ABC
from enum import Enum, auto


class HotDrink(ABC):
    def consume(self):
        pass


class Tea(HotDrink):
    def consume(self):
        print("This tea is delicious")


class Coffee(HotDrink):
    def consume(self):
        print("This coffee is delicious")


class HotDrinkFactory(ABC):
    def prepare(self, amount):
        pass


class TeaFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f"Put in tea bag, boil water," f" pour {amount}ml, enjoy!")
        return Tea()


class CoffeeFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f"Grind some beans, boil water," f" pour {amount}ml, enjoy!")
        return Coffee()


def make_drink(type):
    if type == "tea":
        return TeaFactory().prepare(200)
    elif type == "coffee":
        return CoffeeFactory().prepare(50)
    else:
        return None


class HotDrinkMachine:
    class AvailableDrink(Enum):
        COFFEE = auto()
        TEA = auto()

    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.AvailableDrink:
                name = d.name[0] + d.name[1:].lower()
                factory_name = name + "Factory"
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))

    def make_drink(self):
        print("Available drinks:")
        for idx, f in enumerate(self.factories):
            print(f"{idx}: {f[0]}")

        s = input(f"Please pick drink (0-{len(self.factories) - 1}): ")
        idx = int(s.strip())
        if idx > 1 or idx < 0:
            print("out of range!")
            return -1
        s = input("Specify amount: ")
        amount = int(s.strip())
        return self.factories[idx][1].prepare(amount)


if __name__ == "__main__":
    entry = input("What kind of drink would you like?")
    drink = make_drink(entry.strip())
    if drink:
        drink.consume()

    hdm = HotDrinkMachine()
    hdm.make_drink()
