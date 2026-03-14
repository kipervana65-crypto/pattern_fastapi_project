from fastapi import FastAPI
from .api.auth import router as auth_router
from .api.users import router as user_router
from .db.session import engine
from .db.session import Base

app = FastAPI(title="Auth API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Auth API"}
