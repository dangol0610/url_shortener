class URLServiceError(Exception):
    """Базовое исключение сервиса."""

    pass


class DatabaseError(URLServiceError):
    """Ошибка базы данных."""

    pass


class UrlNotFoundError(URLServiceError):
    """Оригинальный URL не найден."""

    pass
