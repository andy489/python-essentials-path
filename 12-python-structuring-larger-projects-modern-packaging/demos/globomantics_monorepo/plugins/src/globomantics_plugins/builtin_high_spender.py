class HighSpenderDiscount:
    name = "high-spender"

    def apply(self, customer, amount, tier):
        if customer.spend_last_12m >= 3000:
            return max(amount - 25.0, 0)
        return amount
