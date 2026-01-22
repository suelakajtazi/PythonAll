from database import get_connection
from models import BookCreate

class BookService:

    def create_book(self, user_id: int, book: BookCreate):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO books (user_id, title, author, status, rating, review)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, book.title, book.author, book.status, book.rating, book.review))

        conn.commit()
        conn.close()

    def get_books(self, user_id: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM books WHERE user_id=?", (user_id,))
        books = cur.fetchall()

        conn.close()
        return books
