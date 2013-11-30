from flask import Flask
from flask import request, render_template
from flask_sockets import Sockets

from omnithinker import neuter_monkey
from omnithinker.connection import Connection

app = Flask(__name__)
sockets = Sockets(app)
neuter_monkey()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Write document page
@app.route("/write")
def write():
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
