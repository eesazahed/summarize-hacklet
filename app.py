from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_URL = "https://ai.hackclub.com/chat/completions"

BOOKMARKLET = """
javascript:(()=>{let e="https://cdn.jsdelivr.net/gh/eesazahed/summarize-hacklet@latest/bookmarklet/popup.min.css",t=t=>{let r=document.querySelector(".summary-popup");r&&r.remove();let a=document.createElement("div");if(a.className="summary-popup",a.innerHTML=`<div class="summary-inner">${t}<button class="summary-close">&times;</button></div>`,!document.querySelector(`link[href="${e}"]`)){let l=document.createElement("link");l.rel="stylesheet",l.href=e,document.head.appendChild(l)}a.querySelector(".summary-close").addEventListener("click",()=>{a.classList.add("fade-out"),setTimeout(()=>a.remove(),300)}),document.body.appendChild(a)},r=e=>e.replace(/^### (.*$)/gim,"<h3>$1</h3>").replace(/^## (.*$)/gim,"<h2>$1</h2>").replace(/^# (.*$)/gim,"<h1>$1</h1>").replace(/\*\*(.*?)\*\*/gim,"<strong>$1</strong>").replace(/\*(.*?)\*/gim,"<em>$1</em>").replace(/^- (.*$)/gim,"<ul><li>$1</li></ul>").replace(/\n/gim,"<br>"),a=window.getSelection().toString().trim();if(""===a){t("You need to select some text to summarize.");return}t("Generating summary..."),fetch("https://summarize-hacklet.vercel.app/api",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:a})}).then(e=>e.json()).then(e=>{if(!e.summary){t("No summary returned.");return}let a=r(e.summary);t(`<div class="popup-content">${a}</div>`)}).catch(e=>{t(`Error: ${e}`)})})();
"""

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
