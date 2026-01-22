from fastapi import APIRouter
from models import BookCreate
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.post("/{user_id}")
def add_book(user_id: int, book: BookCreate):
    service.create_book(user_id, book)
    return {"message": "Book added"}

@router.get("/{user_id}")
def get_books(user_id: int):
    return service.get_books(user_id)
