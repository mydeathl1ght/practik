import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Таблицы в базе:", tables)

cursor.execute("PRAGMA table_info(tasks)")
columns = cursor.fetchall()
print("Структура таблицы tasks:")
for column in columns:
    print(column)

conn.close()
