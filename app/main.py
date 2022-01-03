from functools import lru_cache
from typing import List, Tuple

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers.accidents import router as accidents_router
from settings import Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

description = """
A simple API to retrieve accidents data from Open Data BCN. 🚀

[Open Data BCN](https://opendata.bcn.cat/) is a free and open data portal for Barcelona.

This API does queries regarding accidents occurred in BCN in several years.

## Items

You can

- Read items
- Create items
- Update items
- Delete items

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "default",
        "description": "Basic endpoint to test and print debug information about the API.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


def create_application() -> FastAPI:
    app = FastAPI(
        title="Accidents API",
        description=description,
        version="0.1.0",
        terms_of_service="",
        contact={
            "name": "Alejandro Aceituna Cano",
            "email": "dev@aacecan.com",
            "url": "https://github.com/aacecandev/core-project-one",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        openapi_tags=tags_metadata,
    )
    app.include_router(accidents_router, prefix="/accidents", tags=["accidents"])
    app.router.redirect_slashes = False
    return app


app = create_application()


@app.on_event("startup")
async def startup():
    if settings.DEBUG:
        print(settings)


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")


@app.get(
    "/",
    summary="Test the API status",
    response_description="Test API connectivity. Doesn't return anything.",
    responses={
        204: {
            "description": "The API is up and running.",
        },
    },
)
async def hello_world():
    """
    This endpoints is only for testing purposes.

    It returns a message when the API is ready to serve requests.
    """
    return JSONResponse(status_code=200)


@app.get("/info")
async def info():
    """
    This endpoint returns information about the application setup parameters

    - DEBUG
    - ENVIRONMENT
    - MAX_CONNECTIONS_COUNT
    - MIN_CONNECTIONS_COUNT
    """
    return {
        "debug": settings.DEBUG,
        "environment": settings.ENVIRONMENT,
        "max_connections_count": settings.MAX_CONNECTIONS_COUNT,
        "min_connections_count": settings.MIN_CONNECTIONS_COUNT,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0")
