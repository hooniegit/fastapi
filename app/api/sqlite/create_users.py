import sqlite3
import os

# open conn
conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/user.db")
cursor = conn.cursor()

# define queries
query_wal = "PRAGMA journal_mode=WAL;"
query_create = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(20),
    password VARCHAR(20)
);
"""
query_insert = """
INSERT INTO users 
VALUES ('hooniegit', '12345678')
"""

# execute queries
cursor.execute(query_wal)
conn.commit()
cursor.execute(query_create)
conn.commit()
cursor.execute(query_insert)
conn.commit()

# close conn
conn.close()
