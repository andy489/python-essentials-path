class Student:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Student({self.name})"


class SqlResult:
    def __init__(self, data: set[Student]):
        self._data = data

    def first(self) -> Student:
        return next(iter(self._data))

    def __len__(self) -> int:
        return len(self._data)


def run_sql_query(query: str) -> SqlResult:
    return SqlResult({Student("Alice"), Student("Bob"), Student("Charlie")})


def get_students(query: str) -> list[Student] | Student | None:
    results = run_sql_query(query)
    if not results:
        return None
    if len(results) == 1:
        return results.first()
    else:
        return list(results._data)


# Better: always return a list
def get_students(query: str) -> list[Student]:
    results = run_sql_query(query)
    if not results:
        return []
    if len(results) == 1:
        return [results.first()]
    else:
        return list(results._data)


print(get_students("SELECT * FROM students WHERE grade > 90"))
