import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Таблицы в базе:", cursor.fetchall())
cursor.execute("PRAGMA table_info(tasks)")
print("Структура таблицы tasks:")
for column in cursor.fetchall():
    print(column)
conn.close()
