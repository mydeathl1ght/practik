import sqlite3


def get_connection():
    """Открывает соединение с базой данных app.db."""
    return sqlite3.connect("app.db")


def show_menu():
    print("\n===== СПИСОК ЗАДАЧ =====")
    print("1. Показать все задачи")
    print("2. Добавить задачу")
    print("3. Отметить задачу выполненной")
    print("4. Удалить задачу")
    print("0. Выход")


def list_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("📭 Список пуст. Добавь первую задачу!")
        return

    print("\n--- ТВОИ ЗАДАЧИ ---")
    for task_id, title, status in rows:
        mark = "✅" if status == "done" else "⬜"
        print(f"{task_id:>3}. {mark} {title}  [{status}]")


def add_task():
    title = input("Название задачи: ").strip()
    if not title:
        print("⚠ Название не может быть пустым.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    # Параметризованный запрос защищает от SQL-инъекций.
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    print(f"✅ Задача добавлена. Её id = {new_id}")


def mark_done():
    list_tasks()
    raw = input("Введи id задачи, которую выполнил: ").strip()
    if not raw.isdigit():
        print("⚠ id должен быть числом.")
        return

    task_id = int(raw)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = 'done' WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        print(f"⚠ Задача с id={task_id} не найдена.")
    else:
        print(f"✅ Задача {task_id} отмечена выполненной.")


def delete_task():
    list_tasks()
    raw = input("Введи id задачи для удаления: ").strip()
    if not raw.isdigit():
        print("⚠ id должен быть числом.")
        return

    task_id = int(raw)
    confirm = input(f"Точно удалить задачу {task_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Отменено.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        print(f"⚠ Задача с id={task_id} не найдена.")
    else:
        print(f"🗑 Задача {task_id} удалена.")


def main():
    # Создаём таблицу, если приложение запущено без выполнения первой работы.
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'new'
        )
    """)
    conn.commit()
    conn.close()

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
            print("⚠ Нет такого пункта. Попробуй снова.")


if __name__ == "__main__":
    main()
