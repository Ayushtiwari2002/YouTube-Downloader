document.getElementById('download-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const url = document.getElementById('url-input').value;
    const statusMessage = document.getElementById('status-message');
    const downloadLink = document.getElementById('download-link');
    const responseDiv = document.getElementById('response');

    // Clear previous messages
    statusMessage.textContent = "Processing...";
    downloadLink.href = '';
    responseDiv.classList.remove('hidden');

    // Send request to backend (Assumed Backend URL)
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusMessage.textContent = "Video is ready to download!";
            downloadLink.href = data.downloadUrl;
            downloadLink.textContent = "Download Here";
        } else {
            statusMessage.textContent = "Failed to download the video. Please try again.";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        statusMessage.textContent = "An error occurred. Please try again.";
    });
});
