import collections
from dataclasses import dataclass, field
from order_item import OrderItem
from customer import Customer

def consume(it):
    collections.deque(it, maxlen=0)

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

    @staticmethod
    def mark_backordered(orders, orderid, itemnumber):
        return Order.map(lambda o:

            # copy all orders that do not match the orderid
            o if o.orderid != orderid
                
            # otherwise build a new order with a new order item list
            else (Order(o.orderid, o.shipping_address, o.expedited, o.shipped, o.customer,
                        Order.map(lambda i:
                            # copy the items that don't match
                            i if i.itemnumber != itemnumber
    
                            # otherwise build a new order item setting backordered to True
                            else OrderItem(i.name, i.itemnumber, i.quantity, i.price, True),
    
                            # iterate over all order items
                            o.order_items)
                        )),
                # iterate over all orders
                orders
            )

    @staticmethod
    def _mark_backordered(orders, orderid, itemnumber):
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
    def filter(predicate, it):
        return tuple(filter(predicate, it))

    @staticmethod
    def map(func, it):
        return tuple(map(func, it))  

    @staticmethod
    def get_filtered_info(predicate, func, orders):
        return Order.map(func, Order.filter(predicate, orders))

    @staticmethod
    def get_order_by_id(orderid, orders):
        return tuple(filter(lambda order: order.orderid == orderid, orders))

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
