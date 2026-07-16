from database.db import get_connection


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Chat History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        bot_response TEXT,
        sentiment TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Memory Summary Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        summary TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    print("Tables Created Successfully")


if __name__ == "__main__":
    create_tables()