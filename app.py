import re

from flask import Flask, abort, redirect, render_template, request, session
from flask_sockets import Sockets

from omnithinker import neuter_monkey
from omnithinker.connection import Connection
from omnithinker.database import Database

PORT = 6004

app = Flask(__name__)
app.secret_key = "cy9wuDOTpKKl8waurlOhbuwbKyvsRAQJ"
sockets = Sockets(app)
database = Database("omnithinker.db")
neuter_monkey()

# Home page
@app.route("/")
def home():
    if session.get("username"):
        return redirect("/projects")
    error = session.pop("error", None)
    focus_login = session.pop("focus_login", False)
    return render_template("index.html", error=error, focus_login=focus_login)

# Login redirector
@app.route("/login", methods=["GET", "POST"])
def login():
    session.pop("username", None)
    if request.method == "GET":
        session["focus_login"] = True
        return redirect("/")
    username = request.form.get("username", "").strip()
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
    return redirect("/projects")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    session.pop("username", None)
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username", "").strip()
    email = request.form.get("email").strip()
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    securityq = request.form.get("securityq", "").strip()
    securitya = request.form.get("securitya", "").strip()
    if username and email and password and confirm:
        if password != confirm:
            error = "Your passwords must match."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+$", email):  # Email verification
            error = "Your email address appears to be invalid."
        elif securityq not in ["none", "color", "app", "teacher"]:
            error = "Your must pick from the list of security questions."
        else:
            error = database.register(username, email, password, securityq,
                                      securitya)
    else:
        error = "Some required fields were missing."
    if error:
        return render_template("register.html", error=error)
    session["username"] = username
    return redirect("/projects")

# Logout redirector
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

# Projects page
@app.route("/projects")
def projects():
    username = session.get("username")
    if not username:
        session["focus_login"] = True
        return redirect("/")
    docs = database.get_documents(username)
    return render_template("projects.html", username=username, documents=docs)

# Write document page
@app.route("/write", methods=["GET", "POST"])
@app.route("/write/<docid>")
def write(docid=None):
    username = session.get("username")
    if docid is not None:
        if not database.authorize_document(username, docid):
            abort(403)  # HTTP 403 Forbidden
        document = database.get_document(docid)
        return render_template("write.html", document=document)
    topic = request.form.get("topic", "").strip()
    docid = database.create_document(username, topic)
    return redirect("/write/{0}".format(docid))

# Delete document redirector
@app.route("/delete/<docid>", methods=["POST"])
def delete(docid):
    username = session.get("username")
    if not database.authorize_document(username, docid):
        abort(403)  # HTTP 403 Forbidden
    database.delete_document(docid)
    return redirect("/projects" if username else "/")

# Document server
@app.route("/download/<docid>/<format>")
def download(docid, format):
    username = session.get("username")
    if not database.authorize_document(username, docid):
        abort(403)  # HTTP 403 Forbidden
    document = database.get_document(docid)
    methods = {
        "txt": document.render_txt,
        "pdf": document.render_pdf
    }
    try:
        data, mimetype = methods[format.lower()]()
        response = app.make_response(data)
        response.mimetype = mimetype
        return response
    except KeyError:
        abort(415)  # HTTP 415 Unsupported Media Type

# Web socket for live document updating
@sockets.route("/socket")
def websocket(socket):
    conn = Connection(socket, database)
    try:
        conn.handle()
    finally:
        conn.finish()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
