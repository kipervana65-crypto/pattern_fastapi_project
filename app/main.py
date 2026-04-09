from contextlib import asynccontextmanager

from fastapi import FastAPI
from .api.auth import router as auth_router
from .api.users import router as user_router
from .db.session import engine
from .db.session import Base

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Auth API", lifespan=lifespan)

app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Auth API"}
