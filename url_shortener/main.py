from fastapi import FastAPI
from . import  models
from .database import engine
from .router import create_url, delete_url, admin_access, landing_page, mapping_url


app = FastAPI(title = "Capstone Project(Scissors: A URL Shortening App)")
models.Base.metadata.create_all(bind=engine)


app.include_router(landing_page.router)
app.include_router(create_url.router)
app.include_router(mapping_url.router)
app.include_router(admin_access.router)
app.include_router(delete_url.router)









