from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from controller import heroes_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(heroes_controller)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)