# attribute validation

print('\nAttribute validation')
from dataclasses import dataclass
@dataclass(frozen=True)
class A:
    i: int
    s: str
    b: bool
     
    def __post_init__(self):
        match (self.i, self.s, self.b):
            case(int(i), str(s), bool(b)) if i <= 42 and s:
                pass 
            case (int(i), _, _) if i > 42:
                raise ValueError(f'Bad i {i}: must be 42 or less')
            case (_, str(s), _) if not s:
                raise ValueError(f'Bad s: empty or None')
            case (_, _, b):
                raise ValueError(f'Bad b {b}: must be boolean')            
            case _:
                raise ValueError('Unable to parse arguments')

for a in (1, '2', True), (50, 2, False), (1, "", True), (1, 2, 'boo'):
    try:
        b = A(*a) #type: ignore
    except Exception as e:
        print(e)
