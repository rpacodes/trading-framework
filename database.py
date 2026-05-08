import sqlite3

conn = sqlite3.connect("trades.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pnl REAL,
        setup TEXT,
        note TEXT,
        tv_link TEXT,
        day TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()

def add_trade(pnl, setup, note, tv_link, day, timestamp):
    cursor.execute("""
        INSERT INTO trades (pnl, setup, note, tv_link, day, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (float(pnl), setup, note, tv_link, day, timestamp))
    conn.commit()

def get_trades():
    cursor.execute("""
        SELECT pnl, setup, note, tv_link, day, timestamp
        FROM trades
        ORDER BY id DESC
    """)
    return cursor.fetchall()

def reset_all_trades():
    cursor.execute("DELETE FROM trades")
    conn.commit()