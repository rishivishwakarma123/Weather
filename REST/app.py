from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# الأفضل: use environment variable instead of hardcoding
API_KEY = os.getenv("API_KEY", "e581e0045207efc3c5a4be1b42d7e562")

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                response = requests.get(url, params=params, timeout=5)
                data = response.json()

                if response.status_code == 200 and data.get("cod") == 200:
                    weather = {
                        "city": city.title(),
                        "temp": data["main"]["temp"],
                        "desc": data["weather"][0]["description"]
                    }
                else:
                    weather = {"error": data.get("message", "City not found")}

            except requests.exceptions.RequestException:
                weather = {"error": "API request failed"}

        else:
            weather = {"error": "Please enter a city name"}

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True, port=5000)