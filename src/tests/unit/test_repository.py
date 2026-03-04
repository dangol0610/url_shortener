from unittest.mock import MagicMock

import pytest


class TestURLRepository:
    """Тесты для repository."""

    @pytest.mark.asyncio
    async def test_get_by_original_success(self, mock_session, repository):
        """Получение ссылки по оригинальному URL."""
        original_url = "https://example.com"
        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_original(original_url)

        assert result == mock_model
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_original_not_found(self, mock_session, repository):
        """Ссылка не найдена."""
        original_url = "https://example.com"
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_original(original_url)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_short_url_success(self, mock_session, repository):
        """Получение ссылки по short_url."""
        short_url = "a3f5c2d8"
        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_short_url(short_url)

        assert result == mock_model

    @pytest.mark.asyncio
    async def test_create_success(self, mock_session, repository):
        """Создание ссылки."""
        short_url = "a3f5c2d8"
        original_url = "https://example.com"

        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_result.scalar_one.return_value = mock_model
        mock_session.execute.return_value = mock_result

        result = await repository.create(short_url, original_url)

        assert result == mock_model
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_increment_redirect_count_success(self, mock_session, repository):
        """Увеличение счётчика редиректов."""
        url_id = 1

        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_result.scalar_one.return_value = mock_model
        mock_session.execute.return_value = mock_result

        result = await repository.increment_redirect_count(url_id)

        assert result == mock_model
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
