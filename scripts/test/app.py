from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True).all()  # Get available resolutions
        return render_template('select_quality.html', streams=streams, url=url)
    except Exception as e:
        return f"Error: {e}"

@app.route('/download_video', methods=['POST'])
def download_video():
    url = request.form['url']
    itag = request.form['itag']
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        stream.download()  # Downloads the video in the selected quality
        return "Download completed!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
