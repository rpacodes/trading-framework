import sqlite3

conn = sqlite3.connect("trading_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pnl REAL,
    setup TEXT,
    note TEXT,
    score INTEGER,
    timestamp TEXT
)
""")

def add_trade(pnl, setup, note, score, timestamp):
    cursor.execute("""
        INSERT INTO trades (pnl, setup, note, score, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (pnl, setup, note, score, timestamp))

    conn.commit()


def get_trades():
    cursor.execute("""
        SELECT pnl, setup, note, score, timestamp FROM trades
    """)
    return cursor.fetchall()