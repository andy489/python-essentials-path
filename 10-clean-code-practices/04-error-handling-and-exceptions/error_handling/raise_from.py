class AdditionError(Exception):
    pass


def plus(a, b):
    try:
        return a + b
    except Exception as e:
        raise AdditionError("Error occurred while adding numbers.") from e


print(plus(2, "3"))  # Should raise AdditionError
