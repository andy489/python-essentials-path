import csv
from dataclasses import dataclass
from tramp import tramp


@dataclass
class Employee:
    id: int
    name: str 
    manager: object
 
# load Employee tree from csv file
# sample data

# "year","name","percent","sex"
# 1880,"John",0.081541,"boy"
# 1880,"William",0.080511,"boy"
# 1880,"James",0.050057,"boy"

with open("d:\\temp\\baby-names.csv") as names:
    reader = csv.reader(names)
    name = lambda: next(reader)[1]
    _ = name()

    # build employee tree
    emps = Employee(1, name(), None)
    for i in range(2, 10):
        emps = Employee(i, name(), emps)
    
# function to find n-over    
def nth_over(e, over = 0, curr = None):
    if e is None or over == 0:
        yield e if e else curr
    else:
        yield nth_over(e.manager, over - 1, e)

# use trampoline function instead of pure recursion
print(tramp(nth_over, emps, 5).name) # type: ignore (supress typing error)
