from functools import singledispatch

@singledispatch
def f(arg, *args):
    print(f'({type(arg).__name__}) {arg}; other args {args}')
    
@f.register(int)
def _(arg, *args):
    print(f'I\'m the integer {arg}')
    
@f.register(tuple)
@f.register(list)
def _(arg, *args):
    print(f'I\'m a list or a tuple {arg}')
    
class C:
    def __init__(self) -> None:
        pass

@f.register(C)
def _(arg, *args):
    print('I\'m an instance of class C')
    

for x in 42, 3.14159, [1,2], (3,4,), C(), C:
    f(x)