from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from src.app.schemas import ShortenedURLResponse, ShortenRequest, URLStatsResponse
from src.utils.dependencies import ServiceDependency
from src.utils.exceptions import DatabaseError, UrlNotFoundError

router = APIRouter(tags=["URL Shortener"])


@router.post(
    "/shorten",
    response_model=ShortenedURLResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Сократить URL",
)
async def shorten_url(
    request_body: ShortenRequest,
    service: ServiceDependency,
) -> ShortenedURLResponse:
    """
    Создать короткую ссылку.
    - **url**: Длинная ссылка для сокращения
    """
    try:
        return await service.create_short_url(str(request_body.url))
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error",
        )


@router.get(
    "/{short_id}",
    status_code=status.HTTP_302_FOUND,
    summary="Редирект на оригинальный URL",
)
async def redirect_to_original(
    short_id: str,
    service: ServiceDependency,
) -> RedirectResponse:
    """
    Редирект на оригинальную ссылку.
    - **short_id**: Короткий идентификатор
    """
    try:
        original_url = await service.redirect_to_original(short_id)
        return RedirectResponse(original_url)
    except UrlNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error",
        )


@router.get(
    "/stats/{short_id}",
    response_model=URLStatsResponse,
    summary="Получить статистику",
)
async def get_stats(
    short_id: str,
    service: ServiceDependency,
) -> URLStatsResponse:
    """
    Получить статистику по короткой ссылке.
    - **short_id**: Короткий идентификатор
    """
    try:
        return await service.get_stats(short_id)
    except UrlNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error",
        )
