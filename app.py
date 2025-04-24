from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_URL = "https://ai.hackclub.com/chat/completions"

@app.route("/")
def home():
    return "<p>check out <a href='https://github.com/eesazahed/summarize-hacklet'>github.com/eesazahed/summarize-hacklet</a></p>", 200

@app.route("/api", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return { "message": "error: no text provided" }, 500
    
    prompt = f"Summarize this:\n\n{data['text']}"

    try:
        response = requests.post(
            API_URL,
            headers={ "Content-Type": "application/json" },
            json={ "messages": [{ "role": "user", "content": prompt }] }
        )

        response_data = response.json()
        summary = response_data["choices"][0]["message"]["content"]
        
        return { "summary": summary }, 200

    except Exception as e:
        return { "message": f"error: {str(e)}" }, 500

@app.errorhandler(404)
def page_not_found(e):
    return "<p>page not found<br /><br /><a href='https://github.com/eesazahed/summarize-hacklet'>github.com/eesazahed/summarize-hacklet</a></p>", 404

if __name__ == "__main__":
    app.run(debug=True)
