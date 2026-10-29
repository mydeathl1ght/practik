import sqlite3
from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)

# Путь к базе определяется относительно папки, где лежит app.py.
DB_PATH = Path(__file__).resolve().parent / "app.db"


def get_connection():
    """Открывает соединение и позволяет обращаться к полям строки по имени."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    return render_template("index.html", items=rows)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
