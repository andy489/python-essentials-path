from tramp import tramp

def s(n, acc=0):
    if n == 0:
        yield acc
    else: 
        yield s(n - 1, acc + n)

print(tramp(s, 1000))
