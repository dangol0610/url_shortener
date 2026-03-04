import hashlib
import secrets

from loguru import logger

from src.app.repository import URLRepository


class HashURLUtils:
    @staticmethod
    async def generate_short_url(url: str, repository: URLRepository) -> str:
        """Генерирует короткий URL на основе MD5 хеша, с учетом коллизий."""
        hash_obj = hashlib.md5(url.encode())
        short_url = hash_obj.hexdigest()[:8]
        logger.info(f"Generated short URL: {short_url}")

        existing = await repository.get_by_short_url(short_url)
        if existing and existing.original_url != url:
            logger.warning(f"Collision detected for URL: {url}, using salted hash")
            salted = url + secrets.token_hex(4)
            hash_obj = hashlib.md5(salted.encode())
            short_url = hash_obj.hexdigest()[:8]
            logger.info(f"Generated salted short URL: {short_url}")
        return short_url
