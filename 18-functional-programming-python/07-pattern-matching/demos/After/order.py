from collections import deque, namedtuple
from dataclasses import dataclass, field

from customer import Customer
from order_item import OrderItem


def consume(it):
    deque(it, maxlen=0)

def action_if(f, g, it):
    consume(f(i) for i in it if g(i))

def get_updated_tuple(p, f, it):
    return tuple(f(i) if p(i) else i for i in it)

@dataclass(frozen=True)
class Order:
    # class attribute
    orders: tuple = field(init=False)

     # instance attributes
    orderid: int
    shipping_address: str
    expedited: bool
    shipped: bool
    customer: Customer
    order_items: tuple[OrderItem, ...]
    
    def __post_init__(self):
        match (self.orderid, self.shipping_address, self.expedited, self.shipped, self.customer):
            case (int(), str(), bool(), bool(), Customer()):
                pass
            case (o, str(), bool(), bool(), Customer()):
                raise ValueError(f'Order id {o} is not an integer')
            case (int(), a, bool(), bool(), Customer()):
                raise ValueError(f'Shipping address {a} is not a string')
            case (int(), str(), e, bool(), Customer()):
                raise ValueError(f'Expedited flag {e} is not a boolean')
            case (int(), str(), bool(), s, Customer()):
                raise ValueError(f'Shipped flag {s} is not a boolean')
            case (int(), str(), bool(), bool(), c):
                raise ValueError(f'{c} is not a customer object') 
            case _:
                raise ValueError('Unable to parse arguments')
        
        match self.order_items:
            case tuple(t):
                for oi in t:
                    match oi:
                        case OrderItem():
                            pass
                        case bad:
                            raise ValueError(f'Invalid order item {bad}')
            case _:
                raise ValueError('Order items are not a tuple')

    @staticmethod
    def get_order_details(orders):
        d = namedtuple('OrderDetails', 'orderid, customer, expedited, itemnumber, item, total_price, backordered')
        return (d(o.orderid, o.customer.name, o.expedited, i.itemnumber, i.name, i.price * i.quantity, i.backordered)
            for o in orders for i in o.order_items)
      
    @staticmethod
    def mark_backordered(orders, orderid, itemnumber):
        return get_updated_tuple(
            lambda o: o.orderid == orderid,
            lambda o: 
                Order(o.orderid, o.shipping_address, o.expedited, o.shipped, o.customer,
                get_updated_tuple(
                    lambda i: i.itemnumber == itemnumber,
                    lambda i: OrderItem(i.name, i.itemnumber, i.quantity, i.price, True),
                    o.order_items
                )
            ),
            orders
        )

    @staticmethod
    def notify_backordered(orders, msg):
        # Functional version, using action_if
        action_if(
            lambda o: o.customer.notify(o.customer, msg),
            lambda o: any(i.backordered for i in o.order_items),
            orders)

    @staticmethod
    def test_expedited(order):
        return order.expedited

    @staticmethod
    def test_not_expedited(order):
        return not order.expedited

    @staticmethod
    def get_customer_name(order):
        return order.customer.name

    @staticmethod
    def get_customer_address(order):
        return order.customer.address

    @staticmethod
    def get_shipping_address(order):
        return order.shipping_address     

    @staticmethod
    def get_filtered_info(predicate, func, orders):
        return map(func, filter(predicate, orders))

    @staticmethod
    def get_order_by_id(orderid, orders):
        return filter(lambda order: order.orderid == orderid, orders)

    @staticmethod
    def set_order_expedited(orderid, orders):
        for order in Order.get_order_by_id(orderid, orders):
            order.expedited = True

    @staticmethod
    def get_expedited_orders_customer_names(orders):
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_customer_name,
            orders
        )

    @staticmethod
    def get_expedited_orders_customer_addresses(orders):
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_customer_address,
            orders
        )

    @staticmethod
    def get_expedited_orders_shipping_addresses(orders):
        return Order.get_filtered_info(
            Order.test_expedited,
            Order.get_shipping_address,
            orders)        

    @staticmethod
    def get_not_expedited_orders_customer_names(orders):
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_customer_name,
            orders
        )

    @staticmethod
    def get_not_expedited_orders_customer_addresses(orders):
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_customer_address,
            orders
        )

    @staticmethod
    def get_not_expedited_orders_shipping_addresses(orders):
        return Order.get_filtered_info(
            Order.test_not_expedited,
            Order.get_shipping_address,
            orders
        )
