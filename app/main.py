from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .routes import citizen_router, security_router
from .config import AppInformation

app_information = AppInformation()
app = FastAPI()


@app.get("/")
async def root():
    return {"response": "hello world"}


app.include_router(citizen_router)
app.include_router(security_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    print(dir(AppInformation))

    openapi_schema = get_openapi(
        title=app_information.APP_NAME,
        version=app_information.VERSION,
        description=app_information.DESCRIPTION,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
