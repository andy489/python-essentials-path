class Order:
    # class attribute
    orders: list = []

    # instance attributes
    orderid: int = 0
    shipping_address: str = ''
    expedited: bool = False
    shipped: bool = False
    customer: object = None

    def get_expedited_orders_customer_names(self):
        output = []
        for order in Order.orders:
            if order.expedited:
                output.append(order.customer.name)
        return output

    def get_expedited_orders_customer_addresses(self):
        output = []
        for order in Order.orders:
            if order.expedited:
                output.append(order.customer.address)
        return output

    def get_expedited_orders_shipping_addresses(self):
        output = []
        for order in Order.orders:
            if order.expedited:
                output.append(order.shipping_address)
        return output
