
class Pizza:
    def __init__(self, name, toppings):
        self.name = name
        self.toppings = toppings

    def get_price(self):
        return sum([t.price for t in self.toppings])

    def __str__(self):
        return f"{self.name}: {self.get_price()}"