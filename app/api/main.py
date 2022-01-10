import sentry_sdk
from docs.open_api import custom_openapi
from fastapi import FastAPI
from routers.accidents_crud import router as accidents_crud_router
from routers.api_info import router as api_info_router
from routers.eda import router as eda_router
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from settings import get_settings

settings = get_settings()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_info_router, prefix="/info", tags=["info"])
    app.include_router(
        accidents_crud_router, prefix="/accidents", tags=["accidents_crud"]
    )
    app.include_router(eda_router, prefix="/eda", tags=["eda"])
    app.router.redirect_slashes = False

    return app


app = create_application()

custom_openapi(app)

try:
    app.add_middleware(SentryAsgiMiddleware)
except Exception:
    # pass silently if the Sentry integration failed
    pass


@app.on_event("startup")
async def startup():
    if settings.DEBUG:
        print(settings)


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")


@app.get("/")
async def root():
    return {"message": "success!"}


# Calling this endpoint to see if the setup works. If yes, an error message will show in Sentry dashboard
@app.get("/sentry")
async def sentry():
    raise Exception("Test sentry integration")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
