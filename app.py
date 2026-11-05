import os, sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
DEMO_ADMIN_PASSWORD = os.environ.get("DEMO_ADMIN_PASSWORD")
DB = "instance/tasks.db"
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is required")

def connect():
    os.makedirs("instance", exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with connect() as db:
        db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, category TEXT NOT NULL DEFAULT 'General', done INTEGER NOT NULL DEFAULT 0)")
        if db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
            db.executemany("INSERT INTO tasks(title,category,done) VALUES(?,?,?)", [
                ("Review Docker image security","DevSecOps",0),
                ("Read Trivy scan report","DevSecOps",1),
                ("Prepare workshop README","Study",0)])

@app.route("/")
def index():
    with connect() as db:
        tasks = db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = db.execute("SELECT COUNT(*) FROM tasks WHERE done=1").fetchone()[0]
    return render_template("index.html", tasks=tasks, total=total, completed=completed)

@app.post("/tasks")
def add_task():
    title = request.form.get("title","").strip()
    category = request.form.get("category","General").strip() or "General"
    if title:
        with connect() as db:
            db.execute("INSERT INTO tasks(title,category) VALUES(?,?)",(title,category))
    flash("Task added successfully.")
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    with connect() as db:
        row = db.execute("SELECT done FROM tasks WHERE id=?",(task_id,)).fetchone()
        if row:
            db.execute("UPDATE tasks SET done=? WHERE id=?",(0 if row["done"] else 1,task_id))
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    with connect() as db:
        db.execute("DELETE FROM tasks WHERE id=?",(task_id,))
    return redirect(url_for("index"))

@app.get("/api/health")
def health():
    return jsonify(status="ok", application="FocusBoard")

@app.get("/admin-demo")
def admin_demo():
    if DEMO_ADMIN_PASSWORD and request.args.get("password") == DEMO_ADMIN_PASSWORD:
        return jsonify(message="Demo admin endpoint reached")
    return jsonify(error="unauthorized"), 401

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)