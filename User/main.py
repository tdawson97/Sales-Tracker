import sqlite3
from flask import Flask, jsonify, request, g

DATABASE = "accounts.sqlite"
app = Flask(__name__)

# open the database with flask
def db_open():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# ensure database is closed
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# initialize the database if needed
with app.app_context():
    db_open().cursor().execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

# create a user in the database, returning an integer id or None if the user
# already exists.
def db_create(username: str, password: str) -> int | None:
    db = db_open()
    c = db.cursor()
    res = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if res is not None:
        return None
    res = c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()
    return db_login(username, password)

def db_login(username: str , password: str) -> int | None:
    c = db_open().cursor()
    res = c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    if res is None:
        return None
    return res[0]

def db_change(username: str, password: str, new_password: str) -> int | None:
    db = db_open()
    c = db.cursor()
    user_id = db_login(username, password)
    if user_id is None: return None
    c.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user_id)
    )
    db.commit()
    return user_id

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.post("/create")
def create():
    ctx = request.get_json(silent=True)
    username = ctx["username"]
    password = ctx["password"]
    user_id = db_create(username, password)
    if user_id == None:
        return jsonify(error="Account already exists for username: " + username), 401
    return jsonify({
        "user_id": user_id,
    })

@app.post("/login")
def login():
    ctx = request.get_json(silent=True)
    username = ctx["username"]
    password = ctx["password"]
    user_id = db_login(username, password)
    if user_id == None:
        return jsonify(error="Invalid username or password"), 401
    return jsonify({
        "user_id": user_id,
    })

@app.post("/change")
def change():
    ctx = request.get_json(silent=True)
    username = ctx["username"]
    password = ctx["password"]
    new_password = ctx["new_password"]
    res = db_change(username, password, new_password)
    if res is None:
        return jsonify(error="Invalid username or password"), 401
    return jsonify({
        "user_id": res
    })

if __name__ == "__main__":
  app.run(port=5000, debug=True)
