import hashlib
from database import get_connection

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE username=?",
        (username,)
    )
    user = cur.fetchone()
    conn.close()

    if user and user[1] == hash_password(password):
        return user[0]
    return None
