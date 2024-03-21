from fastapi import APIRouter


router = APIRouter(tags = ["Home Page"])

@router.get("/")
def home():
    return "Welcome to the URL shortener API :)"