from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        filename = "downloaded_video.mp4"

        ydl_opts = {
            "format": "best",
            "outtmpl": filename,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
