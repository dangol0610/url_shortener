from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repository import URLRepository
from src.app.services import URLService
from src.utils.database import get_session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_repository(session: SessionDependency) -> URLRepository:
    """Создание repository."""
    return URLRepository(session)


RepositoryDependency = Annotated[URLRepository, Depends(get_repository)]


def get_service(repository: RepositoryDependency) -> URLService:
    """Создание service."""
    return URLService(repository)


ServiceDependency = Annotated[URLService, Depends(get_service)]
