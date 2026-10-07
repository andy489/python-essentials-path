class LoyalCustomerDiscount:
    name = "loyal-customer"

    def apply(self, customer, amount, tier):
        if tier in ("gold", "platinum"):
            return round(amount * 0.9, 2)
        return amount
