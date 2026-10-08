from order import Order
from customer import Customer
from order_item import OrderItem

def main():
    HoG = Customer('Heart of Gold', 'The Milky Way Galaxy', False)
    Millis = Customer('Milliways Restaurant', 'Magrathea', True)
    Arthur = Customer('Arthur Dent', 'Earth', False)
    drive = OrderItem('Infinite Improbability Drive', 42, 1, 100, True)
    Trillian = OrderItem('Date with Trillian', 43, 42, 1000000, True)
    choc = OrderItem('Chocolate', 44, 200, 250, False)

    ord1 = Order(1, 'Terra', False, False, HoG, (drive,))
    ord2 = Order(2, 'Heart of Gold', True, False, Arthur, (Trillian, choc))
    ord3 = Order(3, 'Magrathea', True, False, Millis, (choc,))

    Order.orders = (ord1, ord2, ord3)
    Order.notify_backordered(Order.orders, "backordered items")
    
    print('\nMark item as backordered')
    Order.orders = Order.mark_backordered(Order.orders, 3, 44)
    Order.notify_backordered(Order.orders, "backordered items")    
    assert(Order.orders[1].order_items[0].backordered)
    pass
main()
