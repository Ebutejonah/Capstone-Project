from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from .config import get_settings
from . import schemas, models
from .database import SessionLocal, engine
from .repository.crud import deactivate_db_url_by_secret_key, get_db_url_by_key, create_db_url, get_db_url_by_secret_key, update_visitor_count
from .repository.qrcode import generate_qr_code
import validators


app = FastAPI(title = "Capstone Project(Scissors: A URL Shortening App)")
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key = db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    qrcode = generate_qr_code(db_url.url)
    return db_url


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url:schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="The provided URL is invalid")
    db_url = create_db_url(db=db, url = url)
    return get_admin_info(db_url)



@app.get("/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo,)
def get_url_info(secret_key: str, request: Request, db: Session=Depends(get_db)):
    if db_url := get_db_url_by_secret_key(db, secret_key = secret_key):
        return get_admin_info(db_url)
    raise_not_found(request)


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db:Session = Depends(get_db)):
    if db_url := deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"You have successfully deleted the shortened URL for: '{db_url.target_url}'"
        return {"detail": message}
    raise_not_found(request)