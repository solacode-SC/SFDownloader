function showDownloadOptions() {
    const videoUrl = document.getElementById('videoUrl').value;
    const videoId = extractVideoId(videoUrl);
    
    if (videoId) {
        const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/0.jpg`;
        document.getElementById('videoThumbnail').src = thumbnailUrl;
        document.getElementById('downloadOptions').classList.remove('hidden');
    } else {
        alert('Please enter a valid YouTube URL');
    }
}

function extractVideoId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}