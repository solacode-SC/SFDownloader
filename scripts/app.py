from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import logging
import os

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory to store downloaded videos
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Filename counter
file_counter = 0

# Serve the HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Mapping of resolutions to quality labels
def map_resolution_to_quality(resolution):
    quality_map = {
        144: '144p',
        240: '240p',
        360: '360p',
        480: '480p',
        720: '720p',
        1080: '1080p',
        1440: '1440p',
        2160: '4K'
    }
    return quality_map.get(resolution, f'{resolution}p')

# Define the progress hook function
def progress_hook(d):
    if d['status'] == 'finished':
        logger.info(f"Done downloading video '{d['filename']}'")

# Endpoint to get available video qualities
@app.route('/qualities', methods=['POST'])
def get_qualities():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    try:
        ydl_opts = {
            'ffmpeg_location': '/usr/bin',  # Update this to the directory containing ffmpeg and ffprobe
            'format': 'bestaudio/best',
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            # Dictionary to store only one format per resolution
            quality_dict = {}
            for fmt in formats:
                height = fmt.get('height')
                if height and 144 <= height <= 2160:
                    if height not in quality_dict:
                        quality_dict[height] = {
                            'quality': map_resolution_to_quality(height),
                            'url': fmt.get('url'),
                            'filesize': fmt.get('filesize')
                        }
            
            # Convert the dictionary to a list
            quality_options = list(quality_dict.values())
        
        return jsonify({'success': True, 'qualities': quality_options})
    except Exception as e:
        logger.error(f"Error fetching qualities: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Endpoint to download the selected video quality
@app.route('/download', methods=['POST'])
def download():
    global file_counter
    data = request.json
    url = data.get('url')
    quality_url = data.get('quality_url')
    if not url or not quality_url:
        return jsonify({'success': False, 'error': 'No URL or quality URL provided'})
    
    try:
        file_counter += 1
        filename = f"video{file_counter}.%(ext)s"  # Unique filename template
        
        ydl_opts = {
            'ffmpeg_location': '/usr/bin',  # Update this to the directory containing ffmpeg and ffprobe
            'outtmpl': os.path.join(DOWNLOAD_DIR, filename),
            'format': 'best',
            'noplaylist': True,
            'progress_hooks': [progress_hook]  # Hook to track progress
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([quality_url])
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

