from flask import Flask
from flask import request, render_template, redirect

# from omnithinker import

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Write document page
@app.route("/write")
def write():
    return render_template("write.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
