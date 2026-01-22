from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class BookCreate(BaseModel):
    title: str
    author: str
    status: str
    rating: Optional[int] = None
    review: Optional[str] = None
