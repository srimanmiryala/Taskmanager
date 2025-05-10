from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    category_counts = db.execute("SELECT category, COUNT(*) as count FROM tasks GROUP BY category").fetchall()
    db.close()
    return render_template("index.html", tasks=tasks, category_counts=category_counts)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    category = request.form["category"]
    db = get_db()
    db.execute("INSERT INTO tasks (task, category, status) VALUES (?, ?, 0)", (task, category))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    db = get_db()
    status = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()["status"]
    new_status = 0 if status == 1 else 1
    db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    db.commit()
    db.close()
    return redirect("/")

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            category TEXT NOT NULL,
            status INTEGER DEFAULT 0
        )
    ''')
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
