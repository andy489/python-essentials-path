
def get_ints(ints, odd=True, even=True):
    if odd and even:
        return [i for i in ints]
    elif odd:
        return [i for i in ints if i % 2]
    elif even:
        return [i for i in ints if not i % 2]
    else:
        return []

def get_even_ints(ints):
    return [i for i in ints if not i % 2]

def get_odd_ints(ints):
    return [i for i in ints if i % 2]

def get_all_ints(ints):
    return list(ints)

def main():
    ints = range(10)
    print(get_ints(ints))
    print(get_ints(ints, even=False))
    print(get_ints(ints, odd=False))
    print(get_even_ints(ints))
    print(get_odd_ints(ints))
    print(get_all_ints(ints))

main()

def f(x):
    return x.g(lambda x: x.good, lambda x: x.member)

import dis

dis.dis(f)
import dis
def l1(x): return x.good
def l2(x): return x.member
def f2(x): return x.g(l1, l2)


dis.dis(f2)
