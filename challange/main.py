from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

# -------------------------
# Create a Note
# -------------------------
@app.post("/notes")
def create_note(note: Note):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (note.title, note.content)
    )
    conn.commit()
    new_id = cursor.lastrowid

    conn.close()
    return {"id": new_id, "title": note.title, "content": note.content}

# -------------------------
# Get All Notes
# -------------------------
@app.get("/notes")
def get_notes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

# -------------------------
# Get One Note
# -------------------------
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()

    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return dict(row)

# -------------------------
# Update a Note
# -------------------------
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    exists = cursor.fetchone()
    if exists is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")

    cursor.execute(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        (note.title, note.content, note_id)
    )
    conn.commit()
    conn.close()

    return {"id": note_id, "title": note.title, "content": note.content}

# -------------------------
# Delete a Note
# -------------------------
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    exists = cursor.fetchone()
    if exists is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")

    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

    return {"status": "deleted"}
