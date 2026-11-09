"""Отчёты и выгрузка XLSX (Радыгин).

ЗАГЛУШКА: текстовый отчёт работает, выгрузка XLSX — задача #8.
"""

from datetime import date

from src.errors import NotReadyError


class ReportService:
    def __init__(self, storage, expenses):
        self.storage = storage
        self.expenses = expenses

    def trip_report_text(self, trip_id):
        """Отчёт по поездке (ТЗ, п. 5). ЗАГЛУШКА минимального вида."""
        trip = self.storage.find(trip_id)
        totals = self.expenses.totals(trip_id)
        start = date.fromisoformat(trip.start_date)
        end = date.fromisoformat(trip.end_date)
        duration = (end - start).days + 1  # включительно
        left = trip.budget - totals["total"]
        if left >= 0:
            balance = f"остаток бюджета: {left} руб."
        else:
            balance = f"ПРЕВЫШЕНИЕ бюджета: {-left} руб."
        lines = [
            f"Поездка №{trip.trip_id}: {trip.name} ({trip.destination})",
            f"Даты: {trip.start_date} — {trip.end_date}, длительность {duration} дн.",
            f"Бюджет: {trip.budget} руб.",
            "Расходы по категориям:",
        ]
        for cat in ("транспорт", "жильё", "питание", "другое"):
            lines.append(f"  {cat}: {totals['by_category'].get(cat, 0)} руб.")
        lines.append(f"Всего расходов: {totals['total']} руб.")
        lines.append(balance)
        return "\n".join(lines)

    def export_xlsx(self, path, expenses):
        """Выгрузка отфильтрованной истории: листы «Данные» и «Итоги» (ТЗ, п. 8).

        ЗАГЛУШКА. Реализует Радыгин (задача #8).
        """
        raise NotReadyError("Выгрузка XLSX ещё не реализована — задача #8")
