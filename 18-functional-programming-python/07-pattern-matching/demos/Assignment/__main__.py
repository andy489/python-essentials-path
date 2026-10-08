from order import Order
from solution import Customer
from solution import OrderItem

def main():
    
    # test customer validation
    for name, addr, ent in ( \
        ('one', 'two', True),
        ('one', 'two', 43),
        (None, 'two', True),
        ('one', '', False),
        ('one', 'two', 'false'),
        ('', '', '')
    ):
        try:
            c = Customer(name=name, address=addr, enterprise=ent)
        except Exception as ex:
            print(ex)
        
    for name, num, qty, price, backo in (
        ('abc', 1, 10, 13.40, False),
        ('', -1, 0, 12, True),
        ('abc', 1, 0, 0, True),
        ('abc', 1, 1, 1, False),
        ('abc', 1, 2, 3., 'false')
    ):
        try:
            o = OrderItem(name, num, qty, price, backo)
        except Exception as ex:
            print(ex)

main()
