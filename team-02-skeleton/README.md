# Планировщик путешествий — команда 2

Консольная программа для хранения поездок, учёта расходов и отчётов.
Спринт УП.04, 09–14 ноября 2026.

## Запуск

    python -m pip install -r requirements.txt
    python -m src.main

## Тесты

    python -m pytest

## Данные

Рабочие данные — CSV (`data/trips.csv`, `data/expenses.csv`),
выгрузка — только XLSX. Пути задаются в `settings.json`.

Примеры файлов для проверки импорта: `data/expenses_example.csv` (корректный),
`data/expenses_bad.csv` (содержит ошибочную строку — файл отклоняется целиком).

## Структура

    src/domain.py      — модели поездки и расхода, список категорий
    src/errors.py      — типы ошибок программы
    src/validation.py  — общие проверки (единые для ручного ввода и импорта)
    src/storage.py     — поездки: создание, поиск, список (заглушка)
    src/expenses.py    — расходы, бюджет, фильтр, импорт (заглушка)
    src/reports.py     — отчёты и выгрузка XLSX (заглушка)
    src/main.py        — меню
    docs/issues.md     — тексты задач для Issues
    docs/test_plan.md  — тестовый план
