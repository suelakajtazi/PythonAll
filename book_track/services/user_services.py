from database import get_connection
from routers.auth import hash_password

class UserService:

    def create_user(self, username: str, password: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )

        conn.commit()
        conn.close()

