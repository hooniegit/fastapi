import sqlite3
import os

# open conn
conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/authentication.db")
cursor = conn.cursor()

# define queries
query_wal = "PRAGMA journal_mode=WAL;"
query_create = """
CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(20),
    password VARCHAR(20),
    client_id VARCHAR(20),
    client_secret VARCHAR(40)
);
"""

# execute queries
cursor.execute(query_wal)
conn.commit()
cursor.execute(query_create)
conn.commit()

# close conn
conn.close()


if __name__ == "__main__":
    # import secrets
    
    # conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/authentication.db")
    # cursor = conn.cursor()

    # client_id = secrets.token_urlsafe(20)
    # client_secret = secrets.token_urlsafe(40)
    
    # query_insert = f"""
    # INSERT INTO user 
    # VALUES ('hooniegit', '12345678', '{client_id}', '{client_secret}')
    # """

    # cursor.execute(query_insert)
    # conn.commit()
    # conn.close()
    
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/authentication.db")
    cursor = conn.cursor()
    
    query_insert = f"""
    SELECT * FROM user
    WHERE username = 'hooniegit'
    """
    
    cursor.execute(query_insert)
    returned = cursor.fetchone()
    conn.close()
    
    print(returned)
    