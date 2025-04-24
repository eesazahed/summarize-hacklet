javascript: (() => {
    const showPopup = (content) => {
      const existing = document.querySelector(".summary-popup");
      if (existing) {
        existing.remove();
      }
  
      const popup = document.createElement("div");
      popup.className = "summary-popup";
      popup.innerHTML = `
        <div class="summary-inner">
          ${content}
          <button class="summary-close">&times;</button>
        </div>
      `;
  
      const style = document.createElement("style");
      style.textContent = `
        .summary-popup {
          position: fixed;
          bottom: 2rem;
          right: 2rem;
          max-width: 90%;
          width: 22.5rem;
          background: #fff;
          border-radius: 1rem;
          box-shadow: 0 1.25rem 2.5rem rgba(0, 0, 0, 0.12);
          font-family: 'Segoe UI', Roboto, sans-serif;
          font-size: 0.9375rem;
          color: #333;
          z-index: 99999;
          overflow: hidden;
          animation: fadeInUp 0.3s ease;
        }
  
        .summary-inner {
          padding: 1.5rem;
          position: relative;
          max-height: 25rem;
          overflow-y: auto;
        }
  
        .summary-inner h2 {
          margin: 0 0 0.625rem;
          font-size: 1.125rem;
          color: #111;
        }
  
        .popup-content {
          line-height: 1.6;
        }
  
        .summary-close {
          position: absolute;
          top: 0.25rem;
          right: 0.75rem;
          background: none;
          border: none;
          font-size: 1.5rem;
          color: #888;
          cursor: pointer;
          transition: color 0.2s;
        }
  
        .summary-close:hover {
          color: #f43f5e;
        }
  
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(1.25rem);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
  
        @keyframes fadeOutDown {
          from {
            opacity: 1;
            transform: translateY(0);
          }
          to {
            opacity: 0;
            transform: translateY(1.25rem);
          }
        }
  
        .fade-out {
          animation: fadeOutDown 0.3s ease forwards;
        }
  
        @media (max-width: 30rem) {
          .summary-popup {
            bottom: 0.625rem;
            right: 0.625rem;
            left: 0.625rem;
            width: auto;
          }
        }
      `;
  
      popup.querySelector(".summary-close").addEventListener("click", () => {
        popup.classList.add("fade-out");
        setTimeout(() => popup.remove(), 300);
      });
  
      document.head.appendChild(style);
      document.body.appendChild(popup);
    };
  
    const markdown = (text) => {
      return text
        .replace(/^### (.*$)/gim, "<h3>$1</h3>")
        .replace(/^## (.*$)/gim, "<h2>$1</h2>")
        .replace(/^# (.*$)/gim, "<h1>$1</h1>")
        .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/gim, "<em>$1</em>")
        .replace(/^- (.*$)/gim, "<ul><li>$1</li></ul>")
        .replace(/\n/gim, "<br>");
    };
  
    const selection = window.getSelection().toString().trim();
  
    if (selection === "") {
      showPopup("You need to select some text to summarize.");
      return;
    }
  
    showPopup("Generating summary...");
  
    fetch("https://summarize-hacklet.vercel.app/api", {
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
        showPopup(`<div class="popup-content">${htmlSummary}</div>`);
      })
      .catch((error) => {
        showPopup(`Error: ${error}`);
      });
  })();
  