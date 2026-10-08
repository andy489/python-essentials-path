from order import Order
from customer import Customer
from order_item import OrderItem
from tramp import tramp

def main():
    HoG = Customer('Heart of Gold', 'The Milky Way Galaxy', False)
    Millis = Customer('Milliways Restaurant', 'Magrathea', True)
    Arthur = Customer('Arthur Dent', 'Earth', False)
    drive = OrderItem('Infinite Improbability Drive', 1, 1, 100, True)
    Trillian = OrderItem('Date with Trillian', 2, 42, 1000000, True)
    choc = OrderItem('Chocolate', 3, 200, 250, False)

    ord1 = Order(1, 'Terra', False, False, HoG, (drive,))
    ord2 = Order(2, 'Heart of Gold', True, False, Arthur, (Trillian, choc))
    ord3 = Order(3, 'Magrathea', True, False, Millis, (choc,))

    Order.orders = (ord1, ord2, ord3)
    Order.notify_backordered(Order.orders, "backordered items")
    Order.orders = Order.mark_backordered(Order.orders, 3, 'CHOC')
    
# Test order validation

    for o in [
        (1, 'Earth', True, True, HoG, (choc,)), # good
        ('1', 'Earth', True, True, HoG, (choc,)),
        (1, 'Earth', 3, True, HoG, (choc,)),
        (1, 'Earth', True, 4, HoG, (choc,)),
        (1, 'Earth', True, True, 5, (choc,)),
        (1, 'Earth', True, True, HoG, 6),
        (1, 'Earth', True, True, HoG, (7,))
        ]:
        
        try:
            new_o = Order(*o)
        except Exception as e:
            print(e)

# use as exercise            
    for o in Order.get_order_details(Order.orders):
        match o.customer, o.total_price, o.expedited:
            case(cust, price, exp) if exp and price < 100:
                print(f'Customer "{cust}" low price ${price}.')
            case(cust, price, exp) if exp and price < 100_000:
                print(f'Customer "{cust}" mid price ${price}.')
            case(cust, price, exp) if exp:
                print(f'Customer "{cust}" high price ${price}.')
                            
    # use for exercise
    from functools import singledispatch
    @singledispatch
    def get_stuff(obj):
        pass

    @get_stuff.register(Order)
    def _(obj):
        print(f'Order for: {obj.customer.name}')

    @get_stuff.register(OrderItem)
    def _(obj):
        print(f'Order Item: {obj.name}')    

    @get_stuff.register(Customer)
    def _(obj):
        print(f'Customer name: {obj.name}')
        print(f'Customer shipping address: {obj.address}')    
        
    get_stuff(Order.orders[0])
    get_stuff(Order.orders[0].order_items[0])
    get_stuff(Order.orders[0].customer)
    
    # change single dispatch to match
    for o in Order.orders[0], Order.orders[0].order_items[0], Order.orders[0].customer:
        match o:
            case Order() as obj:
                print(f'Order {obj.orderid} for: {obj.customer.name}')
            case OrderItem() as obj:
                print(f'Order Item: {obj.name}')
            case Customer() as obj:
                print(f'Customer name: {obj.name}')
                print(f'Customer shipping address: {obj.address}')   
                    
    from collections import deque                   
    def consume(it):
        deque(it, maxlen=0)
        
    def print_info(obj):
        match obj:
            case Order() as obj:
                print(f'Order {obj.orderid} for: {obj.customer.name}')
            case OrderItem() as obj:
                print(f'Order Item: {obj.name}')
            case Customer() as obj:
                print(f'Customer name: {obj.name}')
                print(f'Customer shipping address: {obj.address}')                                                           

    consume(print_info(obj) for obj in[Order.orders[0], Order.orders[0].order_items[0], Order.orders[0].customer])
main()