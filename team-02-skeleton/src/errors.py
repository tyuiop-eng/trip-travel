"""Типы ошибок программы."""


class AppError(Exception):
    """Базовая ошибка: показывается пользователю без трассировки."""


class ValidationError(AppError):
    """Неверные данные от пользователя или в файле."""


class NotFoundError(AppError):
    """Объект не найден (неизвестный номер поездки)."""


class NotReadyError(AppError):
    """Заглушка: функция ещё не реализована."""


class StorageError(AppError):
    """Не удалось прочитать или сохранить файл."""
