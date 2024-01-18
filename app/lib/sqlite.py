import sqlite3

def execute_query(dir: str, QUERY: str):
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    
    cursor.execute(QUERY)
    conn.commit()
    conn.close()

def fetchall_query(dir: str, QUERY: str, values: tuple):
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    
    cursor.execute(QUERY, values)
    returned = cursor.fetchall()
    
    return returned
    
def fetchone_query(dir: str, QUERY: str, values: tuple):
    conn = sqlite3.connect(dir)
    cursor = conn.cursor()
    
    cursor.execute(QUERY, values)
    returned = cursor.fetchone()
    
    return returned
