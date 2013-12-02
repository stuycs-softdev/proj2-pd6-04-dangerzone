from flask import Flask, flash, redirect, render_template, request, session
from flask_sockets import Sockets

from omnithinker import neuter_monkey
from omnithinker.connection import Connection
from omnithinker.database import Database

app = Flask(__name__)
app.secret_key = "cy9wuDOTpKKl8waurlOhbuwbKyvsRAQJ"
sockets = Sockets(app)
database = Database("omnithinker.db")
neuter_monkey()

# Home page
@app.route("/")
def home():
    error = session.pop("error", None)
    focus_login = session.pop("focus_login", False)
    return render_template("index.html", error=error, focus_login=focus_login)

# Login redirector
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["focus_login"] = True
        return redirect("/")
    username = request.form.get("username").strip()
    password = request.form.get("password")
    if username and password:
        error = database.login(username, password)
    else:
        error = "A username and password are required."
    if error:
        session["focus_login"] = True
        session["error"] = error
        return redirect("/")
    session["username"] = username
    flash(u"Welcome, {0}!".format(username))
    return redirect("/projects")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

# Write document page
@app.route("/write", methods=["GET", "POST"])
def write():
    topic = request.form.get("topic")
    return render_template("write.html")

# ***TEST*** page for Ben's socket protocol
@app.route("/ben-socket-test")
def test():
    return render_template("ben-socket-test.html")

@sockets.route("/socket")
def websocket(socket):
    conn = Connection(socket)
    try:
        conn.handle()
    finally:
        conn.finish()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
