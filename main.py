import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

DATA_FILE_PATH = "src/fastapiprac/data.json"

with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool

def save_data():
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.post("/books", response_model=Book, status_code=201)
async def add_book(book: Book):
    for b in data["books"]:
        if b["id"] == book.id:
            raise HTTPException(status_code=400, detail="Книга с таким ID уже существует")
    data["books"].append(book.model_dump())
    save_data()
    return book

@app.delete("/books/{book_id}", status_code=200)
async def delete_book(book_id: int):
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            data["books"].pop(i)
            save_data()
            return {"detail": "Книга успешно удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            data["books"][i] = updated_book.model_dump()
            save_data()
            return updated_book
    raise HTTPException(status_code=404, detail="Книга не найдена")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)