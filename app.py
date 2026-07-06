import os
from flask import Flask, render_template, jsonify, send_from_directory
from werkzeug.utils import safe_join

app = Flask(__name__)

# Enter your path to the movis and tv shows folder:
# For Linux/Mac
VIDEO_DIR = "/your/directory/path"
# For Windows
# VIDEO_DIR = r"C:\your\directory\path"

# Allowed video extensions
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.webm')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/files')
@app.route('/api/files/')
@app.route('/api/files/<path:subpath>')
def list_files(subpath=""):
    # Securely resolve and join the target directory path
    target_dir = safe_join(VIDEO_DIR, subpath)

    if not target_dir or not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        return jsonify({"error": "Folder not found"}), 404

    items = []

    try:
        for entry in os.scandir(target_dir):
            relative_item_path = os.path.relpath(entry.path, VIDEO_DIR).replace("\\", "/")

            # check if it`s a directory
            if entry.is_dir():
                items.append({
                    "name": entry.name,
                    "type": "folder",
                    "path": relative_item_path
                })
            # check if it`s video file
            elif entry.is_file() and entry.name.lower().endswith(VIDEO_EXTENSIONS):
                items.append({
                    "name": entry.name,
                    "type": "video",
                    "path": relative_item_path,
                    "url": f"/video-stream/{relative_item_path}"
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Group by type and sort alphabetically
    items.sort(key=lambda x: (x['type'] != 'folder', x['name'].lower()))

    return jsonify({
        "current_path": subpath,
        "items": items
    })


# Stream video files in stream
@app.route('/video-stream/<path:filepath>')
def video_stream(filepath):
    return send_from_directory(VIDEO_DIR, filepath)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)