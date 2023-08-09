from fastapi import FastAPI

from config.settings import settings
from routes import bugs, projects, users
from utils.db import init_db


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users.router)
    app.include_router(projects.router)

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def root():
    return {"msg": "hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app", reload=settings.DEBUG, host=settings.HOST, port=settings.PORT
    )
