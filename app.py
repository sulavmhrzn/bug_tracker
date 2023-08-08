from fastapi import FastAPI

from config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI()
    return app


app = create_app()


@app.get("/")
async def root():
    return {"msg": "hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app", reload=settings.DEBUG, host=settings.HOST, port=settings.PORT
    )
