"""
Конфигурация и фикстуры для тестов.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.app.repository import URLRepository
from src.app.services import URLService

# ============================================
# Фикстуры для Repository
# ============================================


@pytest.fixture
def mock_session():
    """Создание mock сессии SQLAlchemy."""
    session = AsyncMock()
    return session


@pytest.fixture
def repository(mock_session):
    """Создание repository с mock сессией."""
    return URLRepository(mock_session)


# ============================================
# Фикстуры для Service
# ============================================


@pytest.fixture
def mock_repository():
    """Создание mock repository."""
    return AsyncMock(spec=URLRepository)


@pytest.fixture
def service(mock_repository):
    """Создание service с mock repository."""
    return URLService(mock_repository)


# ============================================
# Фикстуры для моделей
# ============================================


@pytest.fixture
def mock_url_model():
    """Создание mock модели URL."""
    model = MagicMock()
    model.short_url = "a3f5c2d8"
    model.original_url = "https://example.com"
    model.redirect_count = 0
    model.id = 1
    return model


@pytest.fixture
def mock_existing_url():
    """Создание mock существующей ссылки."""
    model = MagicMock()
    model.short_url = "a3f5c2d8"
    model.original_url = "https://example.com"
    model.redirect_count = 5
    return model
