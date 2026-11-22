from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import Base, engine
from app.routers import prompts

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(prompts.router)