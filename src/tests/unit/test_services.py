from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.app.schemas import ShortenedURLResponse, URLStatsResponse
from src.utils.exceptions import DatabaseError, UrlNotFoundError
from src.utils.hashurl_utils import HashURLUtils


class TestURLService:
    """Тесты для сервиса ссылок."""

    @pytest.mark.asyncio
    async def test_create_short_url_new(self, service, mock_repository):
        """Создание новой ссылки."""
        original_url = "https://example.com"
        short_url = "a3f5c2d8"

        with patch.object(HashURLUtils, "generate_short_url", return_value=short_url):
            mock_repository.get_by_original.return_value = None

            mock_url_model = MagicMock()
            mock_url_model.short_url = short_url
            mock_url_model.original_url = original_url
            mock_url_model.redirect_count = 0
            mock_repository.create.return_value = mock_url_model

            result = await service.create_short_url(original_url)

            assert isinstance(result, ShortenedURLResponse)
            assert result.short_url == short_url
            assert result.original_url == original_url

    @pytest.mark.asyncio
    async def test_create_short_url_existing(
        self, service, mock_repository, mock_existing_url
    ):
        """Создание ссылки, которая уже есть в БД."""
        mock_repository.get_by_original.return_value = mock_existing_url

        result = await service.create_short_url("https://example.com")

        assert isinstance(result, ShortenedURLResponse)
        assert result.short_url == "a3f5c2d8"
        mock_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_redirect_to_original_success(
        self, service, mock_repository, mock_url_model
    ):
        """Успешный редирект."""
        mock_repository.get_by_short_url.return_value = mock_url_model

        result = await service.redirect_to_original("a3f5c2d8")

        assert result == "https://example.com"
        mock_repository.increment_redirect_count.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_redirect_to_original_not_found(self, service, mock_repository):
        """Редирект несуществующей ссылки."""
        mock_repository.get_by_short_url.return_value = None

        with pytest.raises(UrlNotFoundError):
            await service.redirect_to_original("nonexistent")

    @pytest.mark.asyncio
    async def test_get_stats_success(self, service, mock_repository):
        """Успешное получение статистики."""
        mock_url_model = MagicMock()
        mock_url_model.short_url = "a3f5c2d8"
        mock_url_model.original_url = "https://example.com"
        mock_url_model.redirect_count = 42
        mock_url_model.created_at = datetime(2024, 1, 1)
        mock_repository.get_by_short_url.return_value = mock_url_model

        result = await service.get_stats("a3f5c2d8")

        assert isinstance(result, URLStatsResponse)
        assert result.short_url == "a3f5c2d8"
        assert result.redirect_count == 42

    @pytest.mark.asyncio
    async def test_get_stats_not_found(self, service, mock_repository):
        """Статистика несуществующей ссылки."""
        mock_repository.get_by_short_url.return_value = None

        with pytest.raises(UrlNotFoundError):
            await service.get_stats("nonexistent")

    @pytest.mark.asyncio
    async def test_create_short_url_database_error(self, service, mock_repository):
        """Обработка ошибки БД при создании."""

        mock_repository.get_by_original.side_effect = SQLAlchemyError("DB error")

        with pytest.raises(DatabaseError):
            await service.create_short_url("https://example.com")

    @pytest.mark.asyncio
    async def test_redirect_database_error(self, service, mock_repository):
        """Обработка ошибки БД при редиректе."""

        mock_repository.get_by_short_url.side_effect = SQLAlchemyError("DB error")

        with pytest.raises(DatabaseError):
            await service.redirect_to_original("a3f5c2d8")
