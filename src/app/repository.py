from loguru import logger
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import ShortURL


class URLRepository:
    """Repository для работы с короткими ссылками."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_original(self, original_url: str) -> ShortURL | None:
        """Получить модель по оригинальному URL."""
        try:
            query = select(ShortURL).where(ShortURL.original_url == original_url)
            result = await self.session.execute(query)
            logger.info(f"Got by original: {original_url}")
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error while getting by original: {e}")
            raise e

    async def get_by_short_url(self, short_url: str) -> ShortURL | None:
        """Получить модель ссылку по короткому URL."""
        try:
            query = select(ShortURL).where(ShortURL.short_url == short_url)
            result = await self.session.execute(query)
            logger.info(f"Got by short URL: {short_url}")
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Database error while getting by short URL: {e}")
            raise e

    async def create(self, short_url: str, original_url: str) -> ShortURL:
        """Создать новую ссылку."""
        try:
            stmt = (
                insert(ShortURL)
                .values(short_url=short_url, original_url=original_url)
                .returning(ShortURL)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Created short URL: {short_url}")
            return result.scalar_one()
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating: {e}")
            raise e

    async def increment_redirect_count(self, url_id: int) -> ShortURL:
        """Увеличить счетчик редиректов."""
        try:
            stmt = (
                update(ShortURL)
                .where(ShortURL.id == url_id)
                .values(redirect_count=ShortURL.redirect_count + 1)
                .returning(ShortURL)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Incremented redirect count for URL: {url_id}")
            return result.scalar_one()
        except SQLAlchemyError as e:
            logger.error(f"Database error while incrementing redirect count: {e}")
            raise e
