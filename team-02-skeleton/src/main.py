"""Меню программы (Лапатинский). Модули коллег подключены как заглушки.

Проверки ввода выполняются в предметных модулях, а не здесь (ТЗ).
"""

from src.domain import CATEGORIES
from src.errors import AppError, ValidationError
from src.expenses import ExpenseService
from src.reports import ReportService
from src.storage import TripStorage


MENU = (
    "=== Планировщик путешествий ===\n"
    "1. Создать поездку\n"
    "2. Список поездок\n"
    "3. Найти поездку по номеру\n"
    "4. Добавить расход\n"
    "5. Отчёт по поездке\n"
    "6. Импорт расходов из CSV\n"
    "7. История расходов (фильтр)\n"
    "8. Выгрузка истории в XLSX\n"
    "0. Выход\n"
    "Выберите пункт: "
)


def ask(prompt):
    return input(prompt).strip()


def ask_int(prompt):
    text = ask(prompt)
    try:
        return int(text)
    except ValueError:
        raise ValidationError(f"Ожидалось целое число, получено: {text!r}")


def show_trip(trip):
    print(
        f"№{trip.trip_id} | {trip.start_date}–{trip.end_date} | "
        f"{trip.name} | {trip.destination} | бюджет {trip.budget} руб."
    )


def show_expense(e):
    print(f"№{e.expense_id} | поездка №{e.trip_id} | {e.category} | {e.amount} руб.")


def handle(choice, storage, expenses, reports):
    if choice == "1":
        trip_id = storage.add(
            name=ask("Название: "),
            destination=ask("Место назначения: "),
            start_date=ask("Дата начала (ГГГГ-ММ-ДД): "),
            end_date=ask("Дата окончания (ГГГГ-ММ-ДД): "),
            budget=ask("Плановый бюджет (целые рубли): "),
        )
        print(f"Создана поездка №{trip_id}.")
    elif choice == "2":
        trips = storage.list_sorted()
        if not trips:
            print("Поездок пока нет.")
        for trip in trips:
            show_trip(trip)
    elif choice == "3":
        show_trip(storage.find(ask_int("Номер поездки: ")))
    elif choice == "4":
        expense = expenses.add(
            trip_id=ask_int("Номер поездки: "),
            category=ask(f"Категория ({', '.join(CATEGORIES)}): "),
            amount=ask("Сумма (целые рубли): "),
        )
        print(f"Добавлен расход №{expense.expense_id}.")
    elif choice == "5":
        print(reports.trip_report_text(ask_int("Номер поездки: ")))
    elif choice == "6":
        added = expenses.import_csv(ask("Путь к CSV-файлу расходов: "))
        print(f"Добавлено расходов: {added}.")
    elif choice == "7":
        trip_text = ask("Номер поездки (Enter — любая): ")
        category_text = ask("Категория (Enter — любая): ")
        rows = expenses.filter(
            trip_id=int(trip_text) if trip_text else None,
            category=category_text or None,
        )
        if not rows:
            print("Совпадений не найдено.")
        for e in rows:
            show_expense(e)
    elif choice == "8":
        out = reports.export_xlsx(ask("Имя XLSX-файла: "), expenses=expenses.filter())
        print(f"Файл сохранён: {out}")
    else:
        raise ValidationError(f"Нет пункта меню: {choice!r}")


def run():
    storage = TripStorage()
    expenses = ExpenseService(storage)
    reports = ReportService(storage, expenses)
    while True:
        choice = ask(MENU)
        try:
            if choice == "0":
                print("Работа завершена.")
                return
            handle(choice, storage, expenses, reports)
        except (AppError, ValueError) as err:
            print(f"Ошибка: {err}")


if __name__ == "__main__":
    run()
