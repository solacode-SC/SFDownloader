from flask import Flask, request, jsonify, send_from_directory
import instaloader
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

# Define the progress hook function
def progress_hook(filename):
    logger.info(f"Done downloading video '{filename}'")

# Endpoint to get available video qualities
@app.route('/qualities', methods=['POST'])
def get_qualities():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    # Note: Instaloader doesn't provide different video qualities as YouTube does,
    # so we'll skip the quality extraction part and directly provide the URL.
    try:
        # Validate URL and extract media type using Instaloader
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url.split('/')[-2])
        if post.is_video:
            return jsonify({
                'success': True,
                'qualities': [{
                    'quality': 'original',
                    'url': post.video_url,
                    'filesize': None  # Instaloader does not provide file size
                }]
            })
        else:
            return jsonify({'success': False, 'error': 'Not a video post'})
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
        filename = f"video{file_counter}.mp4"  # Unique filename
        
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url.split('/')[-2])
        
        if post.is_video:
            video_url = post.video_url
            # Download the video using requests
            import requests
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                progress_hook(filename)
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Failed to download video'})
        else:
            return jsonify({'success': False, 'error': 'Not a video post'})
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

