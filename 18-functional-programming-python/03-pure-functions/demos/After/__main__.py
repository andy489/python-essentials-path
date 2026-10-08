from order import Order
from customer import Customer

def main():
    cust1 = Customer()
    cust1.name = 'Heart of Gold'
    cust1.address = 'The Milky Way Galaxy'
    cust1.enterprise = False
    cust2 = Customer()
    cust2.name = 'Milliways Restaurant'
    cust2.address = 'Magrathea'
    cust2.enterprise = True

    ord1 = Order()
    ord1.orderid = 41
    ord1.customer = cust1
    ord1.expedited = False
    ord1.shipping_address = 'Infinitely Improbable'

    ord2 = Order()
    ord2.orderid = 42
    ord2.customer = cust2
    ord2.shipping_address = 'Magrathea'

    Order.orders = [ord1, ord2]
    Order.set_order_expedited(ord2.orderid, Order.orders)
    for address in Order.get_expedited_orders_customer_addresses(Order.orders):
        print('Expedited address: ', address)
    for address in Order.get_not_expedited_orders_customer_addresses(Order.orders):
        print('Not expedited address: ', address)

main()
