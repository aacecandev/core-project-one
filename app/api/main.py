from docs.open_api import custom_openapi
from fastapi import FastAPI
from routers.accidents import router as accidents_router
from routers.api_info import router as api_info_router
from settings import get_settings

settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_info_router, prefix="/info", tags=["info"])
    app.include_router(accidents_router, prefix="/accidents", tags=["accidents"])
    app.router.redirect_slashes = False

    return app


app = create_application()

custom_openapi(app)


@app.on_event("startup")
async def startup():
    if settings.DEBUG:
        print(settings)


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
