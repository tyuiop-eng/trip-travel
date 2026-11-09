"""Расходы, бюджет, фильтр, импорт (Ларин).

ЗАГЛУШКА: данные в памяти. Задачи: #3 добавление расхода, #4 расчёт бюджета,
#7 фильтр, #6 импорт CSV (импорт готовит Радыгин — см. issue).
"""

from src import validation
from src.domain import Expense
from src.errors import NotReadyError, NotFoundError


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage
        self._expenses = [
            Expense(1, 1, "транспорт", 3500),
            Expense(2, 1, "питание", 1200),
        ]
        self._next_id = 3

    def add(self, trip_id, category, amount):
        """Добавляет расход к существующей поездке. Ошибка — данные не меняются (ТЗ, п. 3)."""
        if self.storage.find(trip_id) is None:
            raise NotFoundError(f"Поездка №{trip_id} не найдена")
        category = validation.validate_category(category)
        amount = validation.validate_amount(amount)
        expense = Expense(self._next_id, trip_id, category, amount)
        self._next_id += 1
        self._expenses.append(expense)
        return expense

    def totals(self, trip_id):
        """Общая сумма и разбивка по категориям; без расходов — ноль (ТЗ, п. 4)."""
        rows = [e for e in self._expenses if e.trip_id == trip_id]
        by_category = {}
        for e in rows:
            by_category[e.category] = by_category.get(e.category, 0) + e.amount
        return {"total": sum(by_category.values()), "by_category": by_category}

    def filter(self, trip_id=None, category=None):
        """История расходов с фильтрами; пустой фильтр = любое значение (ТЗ, п. 7)."""
        if trip_id is not None:
            if self.storage.find(trip_id) is None:
                raise NotFoundError(f"Поездка №{trip_id} не найдена")
        if category is not None:
            validation.validate_category(category)
        rows = [
            e for e in self._expenses
            if (trip_id is None or e.trip_id == trip_id)
            and (category is None or e.category == category)
        ]
        return sorted(rows, key=lambda e: e.expense_id)

    def import_csv(self, path):
        """Импорт из CSV: атомарно, с отчётом об ошибках по номерам строк (ТЗ, п. 6).

        ЗАГЛУШКА. Реализует Радыгин (задача #6) поверх этого сервиса.
        """
        raise NotReadyError("Импорт из CSV ещё не реализован — задача #6")
