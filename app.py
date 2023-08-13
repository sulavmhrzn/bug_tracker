from fastapi import FastAPI

from config.settings import settings
from routes import bugs, projects, users
from utils.db import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title="Bug Tracker API",
        version="0.1.0",
        description="API for bug tracker frontend",
    )
    app.include_router(users.router)
    app.include_router(projects.router)
    app.include_router(bugs.router)

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
