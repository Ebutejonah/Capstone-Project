from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from ..repository import admin_info
from ..repository.crud import get_db_url_by_secret_key
from url_shortener.database import get_db
from url_shortener import schemas


router = APIRouter(tags=["Admin Access"])


def raise_not_found(request):
    error_message = f"URL '{request.url}' does not exist"
    raise HTTPException(status_code=404, detail=error_message)

@router.get("/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo,)
def get_url_info(secret_key: str, request: Request, db: Session=Depends(get_db)):
    if db_url := get_db_url_by_secret_key(db, secret_key = secret_key):
        return admin_info.get_admin_info(db_url)
    raise_not_found(request)