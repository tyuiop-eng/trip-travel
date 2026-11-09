"""Общие проверки. Правила здесь едины для ручного ввода и импорта (ТЗ).

Минимальные заглушки — дорабатываются в задачах:
#1 validate_trip_fields / validate_budget (Лапатинский),
#3 validate_category / validate_amount (Ларин),
#5 validate_dates (Радыгин).
"""

from datetime import datetime

from src.domain import CATEGORIES
from src.errors import ValidationError


def validate_trip_fields(name, destination, budget):
    if not name.strip():
        raise ValidationError("Название поездки не может быть пустым")
    if not destination.strip():
        raise ValidationError("Место назначения не может быть пустым")
    return validate_budget(budget)


def validate_budget(budget_text):
    try:
        budget = int(budget_text)
    except (TypeError, ValueError):
        raise ValidationError("Бюджет должен быть целым числом")
    if budget <= 0:
        raise ValidationError("Бюджет должен быть положительным целым числом")
    return budget


def validate_dates(start_date, end_date):
    try:
        start = datetime.strptime(str(start_date), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValidationError("Дата начала должна существовать в календаре (формат ГГГГ-ММ-ДД)")
    try:
        end = datetime.strptime(str(end_date), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValidationError("Дата окончания должна существовать в календаре (формат ГГГГ-ММ-ДД)")
    if end < start:
        raise ValidationError("Дата окончания не может предшествовать дате начала")
    return start, end


def validate_category(category):
    if category not in CATEGORIES:
        raise ValidationError("Категория должна быть одной из: " + ", ".join(CATEGORIES))
    return category


def validate_amount(amount_text):
    try:
        amount = int(amount_text)
    except (TypeError, ValueError):
        raise ValidationError("Сумма расхода должна быть целым числом")
    if amount <= 0:
        raise ValidationError("Сумма расхода должна быть положительным целым числом")
    return amount
