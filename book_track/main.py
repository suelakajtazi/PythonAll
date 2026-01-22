from fastapi import FastAPI
from routers import books, auth

app = FastAPI(title="Reading Tracker API")

app.include_router(auth.router)
app.include_router(books.router)
