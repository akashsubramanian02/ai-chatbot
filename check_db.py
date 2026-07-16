from database.db import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

print("\nTables Found:\n")

for table in tables:
    print(table[0])

conn.close()