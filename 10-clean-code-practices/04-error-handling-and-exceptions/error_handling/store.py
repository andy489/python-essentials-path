

products = ["bread", "wine", "coffee"]

try:
    # Just do the work: "happy flow"
    choice = int(input("Select a product [0-2]? "))
    prod = products[choice]
    # Do stuff with product: pack it, send it
except ValueError:
    print("That is not a number")
except IndexError:
    print("Invalid product number")
