from fastapi import APIRouter, HTTPException, Depends
from url_shortener import schemas
from url_shortener.database import get_db
from ..repository.crud import create_db_url
from ..repository import admin_info
from sqlalchemy.orm import Session
import validators


router = APIRouter(tags=["Create Shortened URL"])


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail = message)


@router.post("/url", response_model=schemas.URLInfo)
def create_short_url(url:schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="The provided URL is invalid")
    db_url = create_db_url(db=db, url = url)
    return admin_info.get_admin_info(db_url)
