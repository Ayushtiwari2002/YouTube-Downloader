from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_PATH = "downloads"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"success": False, "message": "Invalid URL"})

    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
            video_info = ydl.extract_info(url, download=False)
            video_title = video_info['title']
            download_file = f"{DOWNLOAD_PATH}/{video_title}.mp4"

        return jsonify({
            "success": True,
            "downloadUrl": f"/files/{video_title}.mp4"
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/files/<filename>')
def serve_file(filename):
    return send_file(f'{DOWNLOAD_PATH}/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
