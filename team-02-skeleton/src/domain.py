"""Модели данных и общий словарь категорий."""

from dataclasses import dataclass


@dataclass
class Trip:
    trip_id: int
    name: str
    destination: str
    start_date: str   # ГГГГ-ММ-ДД
    end_date: str     # ГГГГ-ММ-ДД
    budget: int       # целые рубли


@dataclass
class Expense:
    expense_id: int
    trip_id: int
    category: str
    amount: int      # целые рубли


CATEGORIES = ("транспорт", "жильё", "питание", "другое")
