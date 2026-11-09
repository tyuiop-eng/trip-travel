"""Поездки: создание, поиск, список (Лапатинский).

ЗАГЛУШКА: данные хранятся в памяти с демонстрационными примерами.
Задачи: #1 создание с проверками, #2 поиск и список, #9 сохранение в CSV.
"""

from src import validation
from src.domain import Trip
from src.errors import NotFoundError


SAMPLE_TRIPS = [
    Trip(1, "Казань на выходные", "Казань", "2026-11-20", "2026-11-25", 30000),
    Trip(2, "Карелия осенью", "Сортавала", "2026-11-10", "2026-11-14", 20000),
]


class TripStorage:
    def __init__(self):
        self._trips = {t.trip_id: t for t in SAMPLE_TRIPS}
        self._next_id = max(self._trips) + 1 if self._trips else 1

    def add(self, name, destination, start_date, end_date, budget):
        """Возвращает номер созданной поездки. Ошибочный ввод — ValidationError, запись не создаётся."""
        budget = validation.validate_trip_fields(name, destination, budget)
        validation.validate_dates(start_date, end_date)
        trip = Trip(self._next_id, name.strip(), destination.strip(), start_date, end_date, budget)
        self._next_id += 1
        self._trips[trip.trip_id] = trip
        return trip.trip_id

    def find(self, trip_id):
        trip = self._trips.get(trip_id)
        if trip is None:
            raise NotFoundError(f"Поездка №{trip_id} не найдена")
        return trip

    def list_sorted(self):
        """Сортировка: по дате начала, при равенстве — по номеру (ТЗ, п. 5)."""
        return sorted(self._trips.values(), key=lambda t: (t.start_date, t.trip_id))
