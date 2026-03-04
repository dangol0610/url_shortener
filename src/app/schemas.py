from pydantic import BaseModel, ConfigDict, HttpUrl


class ShortenRequest(BaseModel):
    """Запрос на сокращение ссылки."""

    url: HttpUrl

    model_config = ConfigDict(from_attributes=True)


class ShortenedURLResponse(BaseModel):
    """Ответ с сокращённой ссылкой."""

    short_url: str
    original_url: str

    model_config = ConfigDict(from_attributes=True)


class URLStatsResponse(BaseModel):
    """Ответ со статистикой."""

    short_url: str
    redirect_count: int

    model_config = ConfigDict(from_attributes=True)
