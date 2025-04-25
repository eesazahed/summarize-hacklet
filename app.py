from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_URL = "https://ai.hackclub.com/chat/completions"

@app.route("/")
def home():
    return f"""
        <div style="font-family: sans-serif; margin: 4rem 0; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
            <video height="500" controls autoplay loop muted>
                <source src="https://raw.githubusercontent.com/eesazahed/summarize-hacklet/refs/heads/main/assets/demo.mov" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <br><br>
            <p>
                Access the 
                <a href="https://raw.githubusercontent.com/eesazahed/summarize-hacklet/refs/heads/main/bookmarklet/bookmarklet.min.js" rel="noreferrer" target="_blank">
                    bookmarklet
                </a>
            </p>
            <br>
            <p>
                Check out 
                <a href="https://github.com/eesazahed/summarize-hacklet" rel="noreferrer" target="_blank">
                    github.com/eesazahed/summarize-hacklet
                </a>
            </p>
        </div>
    """, 200

@app.route("/api", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return { "message": "error: no text provided" }, 500
    
    prompt = f"""
                Summarize the following text. 
                Keep the summary concise, but ensure that it conveys all key information. 
                Focus on delivering the most value in the shortest form while preserving important details. 
                Use plain text formatting only, with exceptions for bold, italics, line breaks, and bullet points. No special characters that are not ASCII. 
                (using a single dash followed by a space for bullets, with one line break above and two line breaks below for spacing) where applicable.
                Ensure that no other forms of bullet points are used. Also ensure that no headings or attempted differing font sizes are used either.
                Text to summarize: 
                {data['text']}
            """

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
    return """
        <div style="font-family: sans-serif; margin: 4rem 0; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
            <p>
                Page not found :(
            </p>
            <br>
            <p>
                Check out 
                <a href="https://github.com/eesazahed/summarize-hacklet" rel="noreferrer" target="_blank">
                    github.com/eesazahed/summarize-hacklet
                </a>
            </p>
        </div>
    """, 404

if __name__ == "__main__":
    app.run(debug=True)
