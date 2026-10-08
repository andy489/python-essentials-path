from dataclasses import dataclass

def valid_str(s):
    return isinstance(s, str) and bool(s) 

def valid_int(i):
    return isinstance(i, int) and i > 0

def valid_float(f):
    return isinstance(f, float)  and f > 0

@dataclass(frozen=True)
class Customer():
    name: str
    address: str
    enterprise: bool

    @staticmethod
    def notify(cust, msg):
        print(f'Sending {msg} to {cust.name} at {cust.address}')      

    def __post_init__(self):
        match self.name, self.address, self.enterprise:
            case str(name), str(addr), bool() if name and addr:
                pass
            case name, *_ if not valid_str(name):
                raise ValueError(f'Customer name "{name}" is not a non-empty string')
            case _, addr, _ if not valid_str(addr):
                raise ValueError(f'Customer address "{addr}" is not a non-empty string')
            case _, _, ent:
                raise ValueError(f'Enterprise flag "{ent}" is not a boolean')
            case _:
                raise ValueError("Unable to parse arguments")
        
@dataclass(frozen=True)
class OrderItem:
    name: str
    itemnumber: int
    quantity: int
    price: float
    backordered: bool
    
    @property
    def total_price(self):
        return self.quantity * self.price      
    
    def __post_init__(self):
        match self.name, self.itemnumber, self.quantity, self.price, self.backordered:
            case str(n), int(i), int(q), float(p), bool() if n and i > 0 and q > 0 and p > 0:
                pass
            case n, *_ if not valid_str(n):
                raise ValueError(f'Order item name "{n}" is not a non-empty string')
            case _, i, *_ if not valid_int(i):
                raise ValueError(f'Order item number "{i}" is not a positive integer')
            case _, _, q, *_ if not valid_int(q):
                raise ValueError(f'Order item quantity "{q}" is not a positive integer')
            case _, _, _, p, *_ if not valid_float(p):
                raise ValueError(f'Order item price "{p}" is not a positive float number')
            case _, _, _, _, b:
                raise ValueError(f'Order enterprise flag "{b}" is not a boolean')
            case _:
                raise ValueError("Unable to parse arguments")