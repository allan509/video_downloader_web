from flask import Flask, render_template, request, send_file, redirect, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        try:
            ydl_opts = {
                'outtmpl': 'downloaded_video.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'quiet': True,
                'age_limit': 99,
                'geo_bypass': True,
                'nocheckcertificate': True,
                'restrictfilenames': True,
                'ignoreerrors': True,
                'source_address': '0.0.0.0',
                'postprocessors': [{
                    'key': 'FFmpegVideoConverter',  
                    'preferedformat': 'mp4'
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Find and send the downloaded file
            for ext in ["mp4", "mkv", "webm"]:
                file_name = f"downloaded_video.{ext}"
                if os.path.exists(file_name):
                    return send_file(file_name, as_attachment=True)

            flash("Download completed but file not found.")
        except Exception as e:
            flash(f"Download failed: {str(e)}")

        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

