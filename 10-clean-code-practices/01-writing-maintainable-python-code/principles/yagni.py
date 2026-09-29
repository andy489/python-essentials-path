from abc import ABC, abstractmethod

students = [
    {"name": "Alice", "grades": [85, 90, 78]},
    {"name": "Bob", "grades": [92, 88, 95]},
    {"name": "Charlie", "grades": [70, 75, 80]},
    {"name": "Diana", "grades": [88, 82, 91]},
    {"name": "Ethan", "grades": [95, 100, 98]},
    {"name": "Fiona", "grades": [60, 65, 70]},
    {"name": "George", "grades": [80, 85, 88]},
    {"name": "Paul", "grades": [78, 82, 80]},
]


# Write a simple solution that calculates the average grade of all students.
def average(students: list[dict]) -> dict[str, float]:
    results = {}
    for student in students:
        name = student["name"]
        if student["grades"]:
            avg = sum(student["grades"]) / len(student["grades"])
        else:
            avg = 0.0
        results[name] = avg
    return results


class StatisticsCalculator:
    def __init__(self, strategy: "CalculationStrategy"):
        self.strategy = strategy

    def calculate(
        self, students: list[dict]
    ) -> dict[str, float]:
        return {
            student["name"]: self.strategy.calculate(student["grades"])
            for student in students
        }


class CalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, grades: list[float]) -> float:
        """Calculate a statistic from a list of grades."""
        raise NotImplementedError


class AverageGradeStrategy(CalculationStrategy):
    def calculate(self, grades: list[float]) -> float:
        return sum(grades) / len(grades) if grades else 0.0


class MedianGradeStrategy(CalculationStrategy):
    def calculate(self, grades: list[float]) -> float:
        if not grades:
            return 0.0
        grades.sort()
        mid = len(grades) // 2
        return (
            grades[mid] if len(grades) % 2 == 1 else (grades[mid - 1] + grades[mid]) / 2
        )


class TopGradeStrategy(CalculationStrategy):
    def calculate(self, grades: list[float]) -> float:
        return max(grades) if grades else 0.0


average_calculator = StatisticsCalculator(AverageGradeStrategy())
median_calculator = StatisticsCalculator(MedianGradeStrategy())
top_calculator = StatisticsCalculator(TopGradeStrategy())

print("Average Grades:", average_calculator.calculate(students))
print(average(students))
