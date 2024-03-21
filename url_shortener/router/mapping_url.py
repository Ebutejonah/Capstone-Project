from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from ..repository.crud import update_visitor_count, get_db_url_by_key
from url_shortener.database import get_db
from url_shortener import models

router = APIRouter(tags=["Mapping"])

def raise_not_found(request):
    error_message = f"URL '{request.url}' does not exist"
    raise HTTPException(status_code=404, detail=error_message)

@router.get("/{url_key}")
def forward_to_target_url(url_key:str, request:Request, db:Session=Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()
    if db_url := get_db_url_by_key(db=db, url_key=url_key):
        update_visitor_count(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    raise_not_found(request)