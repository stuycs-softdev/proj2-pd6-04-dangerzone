from flask import Flask
from flask import request, render_template

from omnithinker.server import Server

app = Flask(__name__)

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

if __name__ == "__main__":
    server = Server(host="0.0.0.0", port=5001)
    try:
        server.start()
        app.run(host="0.0.0.0", port=5000)
    finally:
        server.stop()
