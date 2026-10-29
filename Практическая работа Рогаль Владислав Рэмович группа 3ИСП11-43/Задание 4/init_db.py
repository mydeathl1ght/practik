import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'new'
    )
""")
conn.commit()
conn.close()

print("База данных и таблица tasks успешно созданы.")
