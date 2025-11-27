from typing import List,Optional
import sqlite3
from app.models import Item
from app.database import get_db_connection

def create_item(item : Item) -> Item:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name,description) VALUES(?,?)",
        (item.name,item.description)
    )

    conn.commit()
    item.id = cursor.lastrowid
    conn.close()
    return item

def get_item() -> List[Item]:
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items").fetchAll()
    conn.close()
    return [Item(**dict(item)) for item in items]

def get_item(item_id:int) -> Optional[Item]:
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE id=?",(item_id)).fetchone()
    conn.close()
    if item is None:
        return None
    return Item(**dict(item))

def update_items(item_id:int,item:Item) -> Optional[Item]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name=?,description=? WHERE id=?",
        (item.name,item.description,item_id)
    )

    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        return None
    item.id = item_id
    return item

def delete_item(item_id:int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()


    #foto 1 vazhdo