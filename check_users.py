from database.db import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute(
    """
    SELECT
    id,
    username,
    email
    FROM users
    """
)

users = cursor.fetchall()

for user in users:
    print(user)

conn.close()