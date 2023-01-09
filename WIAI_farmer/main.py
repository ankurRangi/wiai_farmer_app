from fastapi import FastAPI
from WIAI_farmer.routers import user, upload, translate
from . import schemas, models
from .utility.database import engine

app = FastAPI()


# To create the table in the database (check the TablePlus)
models.Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Server'])
async def server_setup():
     return {"status": "Ok", "detail": "Working Successfully"}

app.include_router(user.router)
app.include_router(upload.router)
app.include_router(translate.router)

