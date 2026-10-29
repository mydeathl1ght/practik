import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def show_menu():
    print("\n===== СПИСОК ЗАДАЧ =====")
    print("1. Показать все задачи")
    print("2. Добавить задачу")
    print("3. Отметить задачу выполненной")
    print("4. Удалить задачу")
    print("0. Выход")


def list_tasks():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, title, status FROM tasks ORDER BY id").fetchall()
    if not rows:
        print("Список пуст. Добавь первую задачу!")
        return
    for task_id, title, status in rows:
        print(f"{task_id:>3}. {title} [{status}]")


def add_task():
    title = input("Название задачи: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    with get_connection() as conn:
        cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        new_id = cursor.lastrowid
    print(f"Задача добавлена. Её id = {new_id}")


def mark_done():
    list_tasks()
    raw = input("Введи id выполненной задачи: ").strip()
    if not raw.isdigit():
        print("id должен быть числом.")
        return
    with get_connection() as conn:
        cursor = conn.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (int(raw),))
    print("Задача отмечена выполненной." if cursor.rowcount else "Задача не найдена.")


def delete_task():
    list_tasks()
    raw = input("Введи id задачи для удаления: ").strip()
    if not raw.isdigit():
        print("id должен быть числом.")
        return
    task_id = int(raw)
    if input(f"Удалить задачу {task_id}? (y/n): ").strip().lower() != "y":
        print("Отменено.")
        return
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    print("Задача удалена." if cursor.rowcount else "Задача не найдена.")


def main():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'new'
            )
        """)
    while True:
        show_menu()
        choice = input("Выбери действие: ").strip()
        if choice == "1":
            list_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "0":
            print("До встречи!")
            break
        else:
            print("Нет такого пункта. Попробуй снова.")


if __name__ == "__main__":
    main()
