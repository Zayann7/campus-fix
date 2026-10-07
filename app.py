# Cloud Nation | Docker Class | Python Flask application
import platform
import socket
from datetime import datetime

from flask import Flask, jsonify, render_template

app = Flask(__name__)


def server_info():
    return {
        "container": socket.gethostname(),
        "python": platform.python_version(),
        "server": "Flask development server",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.route("/")
def home():
    return render_template("index.html", **server_info())


@app.route("/api/info")
def api_info():
    return jsonify(server_info())


if __name__ == "__main__":
    # host 0.0.0.0 = accept visitors from outside the container
    app.run(host="0.0.0.0", port=5000)
