class Portfolio:
    def __init__(self):
        self.position = {}

    def buy(self, symbol, amount):
        """Buy a certain amount of stock for a given symbol."""
        if symbol not in self.position:
            self.position[symbol] = amount
        else:
            self.position[symbol] += amount


# Let's define some stock prices
current_prices = {"AAPL": 100, "MSFT": 80, "GOOGL": 90}


class Broker:
    """A Broker holds many stock portfolio's and keeps a list of them.
    It can calculate the total value of all portfolio's it holds.
    """

    def __init__(self):
        self.portfolio_list: list[Portfolio] = []

    def new_portfolio(self) -> Portfolio:
        """Create a new portfolio and add it to the list."""
        p = Portfolio()
        self.portfolio_list.append(p)
        return p

    def total_value(self):
        # This function depends on the implementation details of the portfolio
        # When we change the portfolio class, this breaks
        total_value = 0
        for portfolio in self.portfolio_list:
            for symbol, amount in portfolio.position.items():
                value = current_prices[symbol] * amount
                total_value += value
        return total_value


b = Broker()
p = b.new_portfolio()
p.buy("AAPL", 10)
p.buy("MSFT", 5)
p2 = b.new_portfolio()
p2.buy("GOOGL", 8)
print("Total value:", b.total_value())
