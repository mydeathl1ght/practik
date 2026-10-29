import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = "app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создаём таблицу, если база запускается впервые."""
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'В процессе'
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def fetch_all_tasks():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return []
    finally:
        conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if not title:
            return render_template(
                "index.html",
                items=fetch_all_tasks(),
                error="Название задачи не может быть пустым."
            )

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title) VALUES (?)",
                (title,)
            )
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"[DB ERROR] {e}")
            return render_template(
                "index.html",
                items=fetch_all_tasks(),
                error="Не удалось сохранить задачу. Попробуйте ещё раз."
            )
        finally:
            conn.close()

        return redirect(url_for("index"))

    return render_template("index.html", items=fetch_all_tasks())


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
