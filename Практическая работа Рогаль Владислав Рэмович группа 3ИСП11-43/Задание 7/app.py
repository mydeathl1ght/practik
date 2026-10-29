import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "pr7-simple-secret"
DB_PATH = "app.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Создаёт таблицу, если база запускается впервые."""
    connection = get_connection()
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'new'
            )
        """)
        connection.commit()
    finally:
        connection.close()


def fetch_all_tasks():
    connection = get_connection()
    try:
        return connection.execute(
            "SELECT id, title, status FROM tasks ORDER BY id"
        ).fetchall()
    except sqlite3.Error:
        flash("Не удалось загрузить список задач.", "error")
        return []
    finally:
        connection.close()


def insert_task(title):
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        connection.commit()
        return True
    except sqlite3.Error:
        connection.rollback()
        return False
    finally:
        connection.close()


def toggle_task_status(task_id):
    connection = get_connection()
    try:
        cursor = connection.execute("""
            UPDATE tasks
            SET status = CASE
                WHEN status = 'done' THEN 'new'
                ELSE 'done'
            END
            WHERE id = ?
        """, (task_id,))
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error:
        connection.rollback()
        return 0
    finally:
        connection.close()


def delete_task_by_id(task_id):
    connection = get_connection()
    try:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error:
        connection.rollback()
        return 0
    finally:
        connection.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if not title:
            flash("Введите название задачи.", "error")
        elif insert_task(title):
            flash("Задача добавлена.", "success")
            return redirect(url_for("index"))
        else:
            flash("Не удалось сохранить задачу.", "error")

    tasks = fetch_all_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    changed = toggle_task_status(task_id)
    if changed == 0:
        flash(f"Задача #{task_id} не найдена или не удалось изменить её.", "error")
    else:
        flash("Статус задачи изменён.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    deleted = delete_task_by_id(task_id)
    if deleted == 0:
        flash(f"Задача #{task_id} не найдена или не удалось удалить её.", "error")
    else:
        flash("Задача удалена.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
