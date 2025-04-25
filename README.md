# summarize-hacklet

A bookmarklet is a small JavaScript program stored as a browser bookmark. When clicked, it runs code to modify a webpage, extract data, or perform quick actions.

This [bookmarklet](https://github.com/eesazahed/summarize-hacklet/blob/main/bookmarklet/bookmarklet.min.js) creates an AI-generated summary of the selected text when clicked.

<br />

```javascript
javascript:(()=>{try{let e="https://cdn.jsdelivr.net/gh/eesazahed/summarize-hacklet@main/bookmarklet/popup.min.css",t=t=>{let r=document.querySelector(".summary-popup");r&&r.remove();let a=document.createElement("div");if(a.className="summary-popup",a.innerHTML="<div class='summary-inner'>"+t+"<button class='summary-close'>&times;</button></div>",!document.querySelector("link[href='"+e+"']")){let i=document.createElement("link");i.rel="stylesheet",i.href=e,document.head.appendChild(i)}a.querySelector(".summary-close").addEventListener("click",()=>{a.classList.add("fade-out"),setTimeout(()=>a.remove(),300)}),document.body.appendChild(a)},r=e=>e.replace(/\*\*(.*?)\*\*/gim,"<b>$1</b>").replace(/\*(.*?)\*/gim,"<i>$1</i>").replace(/^* (.*$)/gim,"<ul><li>$1</li></ul>").replace(/\n/gim,"<br />"),a=window.getSelection().toString().trim();if(""===a){t("You need to select some text to summarize.");return}t("Generating summary..."),fetch("https://summarize-hacklet.vercel.app/api",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:a})}).then(e=>e.json()).then(e=>{if(!e.summary){t("No summary returned.");return}let a=r(e.summary);t("<div class='popup-content'>"+a+"</div>")}).catch(e=>{t("Error: "+e)})}catch{alert("Could not fetch API")}})();
```

<br />

When the bookmark is clicked, a JavaScript function sends an API request to a Python Flask server, which generates a summary with [ai.hackclub.com](https://ai.hackclub.com/).

Demo:

![image](https://raw.githubusercontent.com/eesazahed/summarize-hacklet/refs/heads/main/assets/demo.gif)

## Note: Some websites, such as GitHub and Gmail, have strict Content Security Policies (CSP) that block outbound requests to external APIs. As a result, this bookmarklet will not work on those sites.

