from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_URL = "https://ai.hackclub.com/chat/completions"

@app.route("/")
def home():
    return {
        "message": "hello world"
    }

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data["text"]:
        return { "message": "error: no text provided" }
    
    prompt = f"Summarize this:\n\n{data['text']}"

    try:
        response = requests.post(
            API_URL,
            headers={ "Content-Type": "application/json" },
            json={ "messages": [{ "role": "user", "content": prompt }] }
        )

        response_data = response.json()
        summary = response_data["choices"][0]["message"]["content"]
        
        return { "summary": summary }

    except Exception as e:
        return { "message": f"error: {str(e)}" }

if __name__ == "__main__":
    app.run(debug=True)