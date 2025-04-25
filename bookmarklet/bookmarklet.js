javascript: (() => {
  try {
  const CSS_URL = "https://cdn.jsdelivr.net/gh/eesazahed/summarize-hacklet@main/bookmarklet/popup.min.css";
  const API_URL = "https://summarize-hacklet.vercel.app/api";

  const showPopup = (content) => {
    const existing = document.querySelector(".summary-popup");
    if (existing) existing.remove();

    const popup = document.createElement("div");
    popup.className = "summary-popup";
    popup.innerHTML = "<div class='summary-inner'>" + content + "<button class='summary-close'>&times;</button></div>";

    if (!document.querySelector("link[href='" + CSS_URL + "']")) {
      const styleLink = document.createElement("link");
      styleLink.rel = "stylesheet";
      styleLink.href = CSS_URL;
      document.head.appendChild(styleLink);
    }

    popup.querySelector(".summary-close").addEventListener("click", () => {
      popup.classList.add("fade-out");
      setTimeout(() => popup.remove(), 300);
    });

    document.body.appendChild(popup);
  };

  const markdown = (text) => {
    return text
      .replace(/\*\*(.*?)\*\*/gim, "<b>$1</b>")
      .replace(/\*(.*?)\*/gim, "<i>$1</i>")
      .replace(/^* (.*$)/gim, "<ul><li>$1</li></ul>")
      .replace(/\n/gim, "<br />");
  };

  const selection = window.getSelection().toString().trim();

  if (selection === "") {
    showPopup("You need to select some text to summarize.");
    return;
  }

  showPopup("Generating summary...");

  fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: selection }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.summary) {
        showPopup("No summary returned.");
        return;
      }

      const htmlSummary = markdown(data.summary);
      showPopup("<div class='popup-content'>" + htmlSummary + "</div>");
    })
    .catch((error) => {
      showPopup("Error: " + error);
    });
  } catch {
    alert("Could not fetch API")
  }
})();
