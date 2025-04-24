# summarize-hacklet

A bookmarklet is a small JavaScript program stored as a browser bookmark. When clicked, it runs code to modify a webpage, extract data, or perform quick actions.

This [bookmarklet](https://github.com/eesazahed/summarize-hacklet/blob/main/bookmarklet/bookmarklet.min.js) creates an AI-generated summary of the selected text when clicked.

When the bookmark is clicked, a JavaScript function sends an API request to a Python Flask server, which generates a summary with [ai.hackclub.com](https://ai.hackclub.com/).

Demo:

![image](https://raw.githubusercontent.com/eesazahed/summarize-hacklet/refs/heads/main/assets/demo.gif)