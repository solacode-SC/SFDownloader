import os
import hashlib
from flask import Flask, render_template, request, send_from_directory
import yt_dlp as youtube_dl

app = Flask(__name__)

# Set the directory where videos will be saved
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Helper function to truncate the video title and make the filename unique
def generate_safe_filename(title, max_length=40):
    # Truncate the title to 100 characters
    truncated_title = title[:max_length]
    
    # Create a hash of the full title to ensure uniqueness
    title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
    
    # Combine truncated title with the hash
    safe_filename = f"{truncated_title}_{title_hash}"
    
    return safe_filename

# Function to download Twitter videos using yt-dlp
def download_twitter_video(url):
    with youtube_dl.YoutubeDL({'format': 'bestvideo+bestaudio/best'}) as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Set download=False to get info without downloading
        video_title = info_dict.get('title', None)
        ext = info_dict.get('ext', 'mp4')  # Get the video extension
    
    # Generate a safe filename
    safe_filename = generate_safe_filename(video_title)
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{safe_filename}.{ext}")
    
    # Download with safe filename
    ydl_opts = {
        'outtmpl': file_path,
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return safe_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            video_title = download_twitter_video(url)
            return render_template('index.html', video_title=video_title)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

# import os
# import hashlib
# from flask import Flask, render_template, request, send_from_directory
# import yt_dlp as youtube_dl

# app = Flask(__name__)

# # Set the directory where videos will be saved
# DOWNLOAD_FOLDER = 'downloads'
# if not os.path.exists(DOWNLOAD_FOLDER):
#     os.makedirs(DOWNLOAD_FOLDER)

# # Helper function to truncate the video title and make the filename unique
# def generate_safe_filename(title, max_length=100):
#     truncated_title = title[:max_length]
#     title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
#     safe_filename = f"{truncated_title}_{title_hash}"
#     return safe_filename

# # Function to download Twitter videos using yt-dlp with resolution or mp3 option
# def download_twitter_video(url, format_option):
#     with youtube_dl.YoutubeDL({'format': format_option}) as ydl:
#         info_dict = ydl.extract_info(url, download=False)
#         video_title = info_dict.get('title', None)
#         ext = 'mp3' if format_option == 'bestaudio' else info_dict.get('ext', 'mp4')

#     safe_filename = generate_safe_filename(video_title)
#     file_path = os.path.join(DOWNLOAD_FOLDER, f"{safe_filename}.{ext}")
    
#     ydl_opts = {
#         'outtmpl': file_path,
#         'format': format_option,
#         'noplaylist': True
#     }
    
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

#     return safe_filename

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         url = request.form['url']
#         resolution = request.form['resolution']
        
#         try:
#             # Check if MP3 was selected
#             format_option = 'bestaudio' if resolution == 'mp3' else f'bestvideo[height={resolution}]+bestaudio/best'
#             video_title = download_twitter_video(url, format_option)
#             return render_template('index.html', video_title=video_title)
#         except Exception as e:
#             return render_template('index.html', error=str(e))
#     return render_template('index.html')

# @app.route('/downloads/<filename>')
# def download_file(filename):
#     return send_from_directory(DOWNLOAD_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True)
