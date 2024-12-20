from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import datetime
import wikipedia
import pyjokes
import pywhatkit
import aiohttp
import asyncio

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# API Keys
NEWS_API_KEY = "e1b9396392044aa5bcecb7f0ab29dbb6"
WEATHER_API_KEY = "029fd7af99a54f22ac6173050240108"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)
engine.setProperty('rate', 140)

def talk(text):
    """Speak the given text aloud."""
    engine.say(text)
    engine.runAndWait()

async def fetch_data(url):
    """Helper function to fetch data from APIs."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None

@app.route("/")
def home():
    """Welcome route."""
    return "Welcome to Zara, your virtual assistant!"

@app.route("/weather", methods=["GET"])
async def weather():
    """Fetch the current weather for a given city."""
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    data = await fetch_data(url)
    if data:
        temperature = data['current']['temp_c']
        location = data['location']['name']
        return jsonify({"weather": f"The temperature in {location} is {temperature} degrees Celsius."})
    return jsonify({"error": "Error fetching weather data."}), 500

@app.route("/news", methods=["GET"])
async def news():
    """Fetch top news headlines."""
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    data = await fetch_data(url)
    if data:
        headlines = [article["title"] for article in data.get("articles", [])[:5]]
        return jsonify({"headlines": headlines})
    return jsonify({"error": "Error fetching news data."}), 500

@app.route("/wikipedia", methods=["GET"])
def wikipedia_summary():
    """Fetch a brief summary from Wikipedia."""
    topic = request.args.get("topic")
    if not topic:
        return jsonify({"error": "Topic not provided"}), 400
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return jsonify({"summary": summary})
    except wikipedia.exceptions.DisambiguationError:
        return jsonify({"error": "Multiple entries found. Please be more specific."}), 400
    except wikipedia.exceptions.PageError:
        return jsonify({"error": "Topic not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Error retrieving information: {e}"}), 500

@app.route("/joke", methods=["GET"])
def joke():
    """Return a random joke."""
    return jsonify({"joke": pyjokes.get_joke()})

@app.route("/time", methods=["GET"])
def time():
    """Return the current time."""
    time_now = datetime.datetime.now().strftime('%I:%M %p')
    return jsonify({"time": time_now})

@app.route("/play", methods=["POST"])
def play():
    """Play a song on YouTube."""
    data = request.get_json()
    song = data.get("song", "")
    if song:
        pywhatkit.playonyt(song)
        return jsonify({"message": f"Playing {song}"})
    return jsonify({"error": "Song not provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
