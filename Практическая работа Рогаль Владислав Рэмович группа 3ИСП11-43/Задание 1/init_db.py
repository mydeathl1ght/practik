import sqlite3

# Подключение к базе данных. Если app.db не существует, SQLite создаст файл.
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Создание таблицы задач. IF NOT EXISTS позволяет запускать скрипт повторно.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'new'
    )
""")

# Сохраняем изменения и закрываем соединение.
conn.commit()
conn.close()

print("База данных и таблица tasks успешно созданы.")
