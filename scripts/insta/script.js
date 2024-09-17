function getQualities() {
    const url = document.getElementById('videoUrl').value;
    fetch('/qualities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        const qualitySelect = document.getElementById('qualitySelect');
        qualitySelect.innerHTML = '<option value="">Select quality</option>'; // Clear existing options
        if (data.success) {
            data.qualities.forEach(quality => {
                const option = document.createElement('option');
                option.value = quality.url;
                const sizeText = quality.filesize ? ` (${formatBytes(quality.filesize)})` : '';
                option.textContent = `${quality.quality}${sizeText}`;
                qualitySelect.appendChild(option);
            });
        } else {
            document.getElementById('message').innerText = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        document.getElementById('message').innerText = 'Network error: ' + error.message;
    });
}

function downloadVideo() {
    const url = document.getElementById('videoUrl').value;
    const qualityUrl = document.getElementById('qualitySelect').value;
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url, quality_url: qualityUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('message').innerText = 'Download started!';
        } else {
            document.getElementById('message').innerText = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        document.getElementById('message').innerText = 'Network error: ' + error.message;
    });
}

// Utility function to format bytes
function formatBytes(bytes) {
    if (bytes === undefined) return 'N/A';
    if (bytes === 0) return '0 Byte';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

