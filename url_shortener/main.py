from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import  models
from .database import engine, get_db
from .repository.crud import  get_db_url_by_key , update_visitor_count
from .router import create_url, delete_url, admin_access, landing_page



app = FastAPI(title = "Capstone Project(Scissors: A URL Shortening App)")
models.Base.metadata.create_all(bind=engine)


app.include_router(landing_page.router)

app.include_router(create_url.router)

app.include_router(admin_access.router)

app.include_router(delete_url.router)






def raise_bad_request(message):
    raise HTTPException(status_code=400, detail = message)


def raise_not_found(request):
    error_message = f"URL '{request.url}' does not exist"
    raise HTTPException(status_code=404, detail=error_message)

@app.get("/{url_key}")
def forward_to_target_url(url_key:str, request:Request, db:Session=Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()
    if db_url := get_db_url_by_key(db=db, url_key=url_key):
        update_visitor_count(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    raise_not_found(request)








