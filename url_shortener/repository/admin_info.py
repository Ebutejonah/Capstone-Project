from url_shortener import schemas, models
from url_shortener.config import get_settings
from starlette.datastructures import URL
from url_shortener import main
from .qrcode import generate_qr_code

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = main.app.url_path_for(
        "administration info", secret_key = db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    qrcode = generate_qr_code(db_url.url)
    return db_url
