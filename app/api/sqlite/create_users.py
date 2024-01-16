import sqlite3

conn = sqlite3.connect("user.db")
cursor = conn.cursor()

query_1 = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(20),
    password VARCHAR(20)
)
"""

query_2 = """
INSERT INTO users 
VALUES ('hooniegit', '12345678')
"""

cursor.execute(query_1)
conn.commit()
cursor.execute(query_2)
conn.commit()
conn.close()
