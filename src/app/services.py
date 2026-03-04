from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.app.repository import URLRepository
from src.app.schemas import ShortenedURLResponse, URLStatsResponse
from src.utils.exceptions import DatabaseError, UrlNotFoundError
from src.utils.hashurl_utils import HashURLUtils


class URLService:
    """Service для работы с короткими ссылками."""

    def __init__(self, repository: URLRepository):
        self.repository = repository

    async def create_short_url(self, original_url: str) -> ShortenedURLResponse:
        """Создать короткую ссылку для оригинальной ссылки."""
        try:
            existing_url = await self.repository.get_by_original(original_url)
            if existing_url:
                logger.info(f"Short URL already exists for {original_url}")
                return ShortenedURLResponse.model_validate(existing_url)
            short_url = await HashURLUtils.generate_short_url(
                original_url,
                self.repository,
            )
            url_model = await self.repository.create(short_url, original_url)
            logger.info(f"Created short URL for {original_url}")
            return ShortenedURLResponse.model_validate(url_model)
        except SQLAlchemyError as e:
            logger.error(f"Failed to create short URL: {e}")
            raise DatabaseError("Can not create short URL")

    async def redirect_to_original(self, short_id: str) -> str:
        """Редирект на оригинальную ссылку по короткому идентификатору."""
        try:
            url_model = await self.repository.get_by_short_url(short_id)
            if not url_model:
                logger.error(f"Original URL not found by short ID: {short_id}")
                raise UrlNotFoundError("Original URL not found")
            await self.repository.increment_redirect_count(url_model.id)
            logger.info(f"Redirecting to original URL: {url_model.original_url}")
            return url_model.original_url
        except SQLAlchemyError as e:
            logger.error(f"Failed to redirect to original URL: {e}")
            raise DatabaseError("Can not redirect to original URL")

    async def get_stats(self, short_id: str) -> URLStatsResponse:
        """Получить статистику по короткому идентификатору."""
        try:
            url_model = await self.repository.get_by_short_url(short_id)
            if not url_model:
                logger.error(f"Not found by short ID: {short_id}")
                raise UrlNotFoundError("URL not found")
            logger.info(f"Getting stats for short URL: {short_id}")
            return URLStatsResponse.model_validate(url_model)
        except SQLAlchemyError as e:
            logger.error(f"Failed to get stats: {e}")
            raise DatabaseError("Can not get stats")
