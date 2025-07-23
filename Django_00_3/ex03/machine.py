from beverages import Coffee, Tea, Chocolate, Cappuccino, HotBeverage
import random

class CoffeeMachine:
    def __init__(self):
        self.use_count = 0
        self.is_broken = False

    class EmptuCup(HotBeverage):
        def __init__(self):
            super().__init__(price=0.90, name="empty cup")

        def description(self):
            return "An empty cup?! Gimme my money back"

    class BrokenMachineException(Exception):
        def __str__(self):
            return "This coffee machine has to be repaired."

    def repair(self):
        self.use_count = 0
        self.is_broken = False
        return "Machine repair"

    def serve(self, beverage: HotBeverage):
        if self.is_broken:
            raise self.BrokenMachineException()

        self.use_count += 1
        if self.use_count > 10:
            self.is_broken = True
            raise self.BrokenMachineException()

        if random.choice([True, False]):
            return beverage
        else:
            return self.EmptuCup()

if __name__ == "__main__":
    machine = CoffeeMachine()
    drinks = [Coffee(), Tea(), Chocolate(), Cappuccino()]
    count = 0

    while count < 3:
        try:
            for _ in range(15):
                drink = machine.serve(random.choice(drinks))
                print(f"Drink is :\n{drink}\n")
        except CoffeeMachine.BrokenMachineException as e:
            print("\nHELP\n")
            print(e)
            print(machine.repair())
            print("\n\n")
            count += 1
        else:
            break