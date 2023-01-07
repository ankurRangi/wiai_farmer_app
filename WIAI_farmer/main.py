from fastapi import FastAPI
from .routers import user
from . import schemas, models
from .database import engine

app = FastAPI()


# To create the table in the database (check the TablePlus)
models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)


