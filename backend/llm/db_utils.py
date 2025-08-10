import sqlite3
from datetime import datetime

DB_NAME = "rag_app.db"

def get_db_connection():
    print("Get connection")
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_appl_logs():
    conn = get_db_connection()

    conn.execute('''Create table if not exists application_logs                    
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     user_query TEXT,
                     gpt_response TEXT,
                     model TEXT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
def insert_appl_logs(session_id,question,answer,model):
    conn = get_db_connection()

    conn.execute(' insert into application_logs(session_id, user_query, gpt_response, model) values(?,?,?,?)',[session_id,question,answer,model])
    conn.commit()
    conn.close()

    print('logs saved')


def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('select session_id, user_query, gpt_response, model from application_logs where session_id = (?)',[session_id])

    rows = cursor.fetchall()
    messages = []

    for row in rows:
        messages.extend([
            {"role":"human","content":row['user_query']},
            {"role":"ai","content":row['gpt_response']}
        ])

    conn.close()

    return messages

create_appl_logs()