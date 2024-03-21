from fastapi import APIRouter, HTTPException, Depends, Request
from url_shortener.database import get_db
from ..repository.crud import deactivate_db_url_by_secret_key
from sqlalchemy.orm import Session



router = APIRouter(tags=["Delete Shortened URL"])


def raise_not_found(request):
    error_message = f"URL '{request.url}' does not exist"
    raise HTTPException(status_code=404, detail=error_message)

@router.delete("/admin/{secret_key}")
def delete_short_url(secret_key: str, request: Request, db:Session = Depends(get_db)):
    if db_url := deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"You have successfully deleted the shortened URL for: '{db_url.target_url}'"
        return {"detail": message}
    raise_not_found(request)
