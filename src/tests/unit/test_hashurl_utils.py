import hashlib
from unittest.mock import MagicMock

import pytest

from src.utils.hashurl_utils import HashURLUtils


class TestHashURLUtils:
    """Тесты для утилит генерации short_url."""

    @pytest.mark.asyncio
    async def test_generate_short_url_format(self, mock_repository):
        """Проверка формата short_url (8 символов, hex)."""
        url = "https://example.com"
        mock_repository.get_by_short_url.return_value = None

        result = await HashURLUtils.generate_short_url(url, mock_repository)

        assert len(result) == 8
        assert all(c in "0123456789abcdef" for c in result)

    @pytest.mark.asyncio
    async def test_generate_short_url_deterministic(self, mock_repository):
        """Одинаковый URL → одинаковый short_url (без коллизий)."""
        url = "https://example.com"
        mock_repository.get_by_short_url.return_value = None

        result1 = await HashURLUtils.generate_short_url(url, mock_repository)
        result2 = await HashURLUtils.generate_short_url(url, mock_repository)

        assert result1 == result2

    @pytest.mark.asyncio
    async def test_generate_short_url_with_collision(self, mock_repository):
        """Генерация с коллизией — должна добавить соль."""
        url = "https://example.com"

        # Коллизия (existing с другим URL)
        colliding_model = MagicMock()
        colliding_model.original_url = "https://different.com"
        mock_repository.get_by_short_url.return_value = colliding_model

        result = await HashURLUtils.generate_short_url(url, mock_repository)

        assert len(result) == 8
        # Проверяем, что get_by_short_url вызвался 1 раз
        assert mock_repository.get_by_short_url.call_count == 1

    @pytest.mark.asyncio
    async def test_generate_short_url_no_collision(self, mock_repository):
        """Генерация без коллизии — соль не нужна."""
        url = "https://example.com"
        mock_repository.get_by_short_url.return_value = None

        result = await HashURLUtils.generate_short_url(url, mock_repository)

        assert len(result) == 8
        assert mock_repository.get_by_short_url.call_count == 1

    @pytest.mark.asyncio
    async def test_generate_short_url_same_url_returns_same_hash(self, mock_repository):
        """Тот же URL в БД — возвращаем тот же hash (не коллизия)."""
        url = "https://example.com"

        existing_model = MagicMock()
        existing_model.original_url = url
        mock_repository.get_by_short_url.return_value = existing_model

        result = await HashURLUtils.generate_short_url(url, mock_repository)

        expected = hashlib.md5(url.encode()).hexdigest()[:8]
        assert result == expected
