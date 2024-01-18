
def execute_query(dir: str, QUERY: str):
    import sqlite3

    # open conn
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()

    # execute queries
    cursor.execute(QUERY)
    conn.commit()

    # close conn
    conn.close()


if __name__ == "__main__":
    import secrets, os
    
    dir = os.path.dirname(os.path.abspath(__file__)) + "/authentication.db"
    
    QUERY_WAL = "PRAGMA journal_mode=WAL;"
    QUERY_CREATE = f"""CREATE TABLE IF NOT EXISTS user (
        usermane VARCHAR(20),
        password VARCHAR(20),
        client_id VARCHAR(20),
        client_secret VARCHAR(40)
        )"""

    client_id = secrets.token_urlsafe(20)
    client_secret = secrets.token_urlsafe(40)
    QUERY_INSERT = f"""
    INSERT INTO user 
    VALUES ('<username>', '<password>', '{client_id}', '{client_secret}')
    """
    
    execute_query(dir=dir, QUERY=QUERY_WAL)
    execute_query(dir=dir, QUERY=QUERY_CREATE)
    execute_query(dir=dir, QUERY=QUERY_INSERT)
    
    