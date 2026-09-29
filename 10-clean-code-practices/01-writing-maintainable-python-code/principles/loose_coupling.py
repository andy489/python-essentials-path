class Portfolio:
    def __init__(self):
        self.position = {}

    def buy(self, symbol, amount):
        if symbol not in self.position:
            self.position[symbol] = amount
        else:
            self.position[symbol] += amount

    def value(self):
        """Return total value using a price lookup (mapping or callable)."""
        total = 0
        for symbol, amount in self.position.items():
            total += current_prices[symbol] * amount
        return total


# Let's define some stock prices
current_prices = {"AAPL": 100, "MSFT": 80, "GOOGL": 90}


class Broker:
    """Broker no longer depends on Portfolio internals; it asks each portfolio for its value."""

    def __init__(self):
        self.portfolio_list: list[Portfolio] = []

    def new_portfolio(self) -> Portfolio:
        p = Portfolio()
        self.portfolio_list.append(p)
        return p

    def total_value(self):
        return sum(p.value() for p in self.portfolio_list)


b = Broker()
p = b.new_portfolio()
p.buy("AAPL", 10)
p.buy("MSFT", 5)
p2 = b.new_portfolio()
p2.buy("GOOGL", 8)

print("Total value:", b.total_value())
