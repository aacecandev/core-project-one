from fastapi.responses import JSONResponse
from routers.api_router import APIRouter, TimedRoute
from settings import get_settings

settings = get_settings()

router = APIRouter(
    tags=["info"],
    route_class=TimedRoute,
)


@router.get(
    "/",
    summary="Test the API status",
    response_description="Test API connectivity. Doesn't return anything.",
    responses={
        200: {
            "description": "The API is up and running.",
        },
    },
)
async def root() -> JSONResponse:
    """
    This endpoints is only for testing purposes.

    It returns a message when the API is ready to serve requests.
    """
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome to OpenDataBCN API!"},
    )


@router.get(
    "/variables",
    summary="Get the API variables",
)
async def info() -> JSONResponse:
    """
    This endpoint returns information about the application setup parameters

    - DEBUG
    - ENVIRONMENT
    - MAX_CONNECTIONS_COUNT
    - MIN_CONNECTIONS_COUNT
    """
    return JSONResponse(
        status_code=200,
        content={
            "debug": settings.DEBUG,
            "environment": settings.ENVIRONMENT,
            "max_connections_count": settings.MAX_CONNECTIONS_COUNT,
            "min_connections_count": settings.MIN_CONNECTIONS_COUNT,
        },
    )
