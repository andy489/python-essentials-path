def f(x, y):
    return x*y

def f2(x):
    def _(y):
        return f(x, y)
    return _

def g(x, y, z):
    return x * y - z

def g1(x, y):
    return lambda z: g(x, y, z)

def g2(x):
    return lambda y: g1(x, y)


print(f2(2))
print(f2(2)(3))

print (g(1, 2, 3))
print (g1(1, 2)(3))
print (g2(1)(2)(3))
