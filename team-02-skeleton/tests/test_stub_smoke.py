"""Дымовые проверки каркаса (QA). Заменяются реальными тестами задач #1–#8."""

import pytest

from src.errors import NotFoundError, ValidationError
from src.expenses import ExpenseService
from src.storage import TripStorage


def make_services():
    storage = TripStorage()
    return storage, ExpenseService(storage)


def test_create_and_find_trip():
    storage, _ = make_services()
    trip_id = storage.add("Тест", "Суздаль", "2026-11-20", "2026-11-22", "15000")
    assert storage.find(trip_id).destination == "Суздаль"


def test_expense_and_totals():
    storage, expenses = make_services()
    trip_id = storage.add("Тест", "Суздаль", "2026-11-20", "2026-11-22", "15000")
    expenses.add(trip_id, "питание", "1000")
    expenses.add(trip_id, "транспорт", "2500")
    totals = expenses.totals(trip_id)
    assert totals["total"] == 3500
    assert totals["by_category"]["питание"] == 1000


def test_totals_without_expenses_are_zero():
    storage, expenses = make_services()
    trip_id = storage.add("Пустая", "Тула", "2026-12-01", "2026-12-02", "10000")
    assert expenses.totals(trip_id)["total"] == 0


def test_reject_bad_trip_fields():
    storage, _ = make_services()
    with pytest.raises(ValidationError):
        storage.add("", "Тула", "2026-11-20", "2026-11-22", "15000")
    with pytest.raises(ValidationError):
        storage.add("Тест", "Тула", "2026-11-20", "2026-11-22", "-5")
    with pytest.raises(ValidationError):
        storage.add("Тест", "Тула", "2026-02-30", "2026-11-22", "15000")


def test_reject_bad_expense_and_unknown_trip():
    storage, expenses = make_services()
    with pytest.raises(ValidationError):
        expenses.add(1, "еда", "100")      # недопустимая категория
    with pytest.raises(NotFoundError):
        expenses.add(999, "питание", "100")  # неизвестная поездка


def test_list_sorted_by_date_then_id():
    storage, _ = make_services()
    ids = [t.trip_id for t in storage.list_sorted()]
    assert ids == sorted(ids)  # демонстрационные примеры отсортированы по дате
