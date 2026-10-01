from flask import Blueprint, render_template, jsonify, send_from_directory
from flask import current_app
from werkzeug.utils import safe_join
import os


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/api/files')
@main_bp.route('/api/files/')
@main_bp.route('/api/files/<path:subpath>')
def list_files(subpath=""):
    video_dir = current_app.config.get('VIDEO_DIR')
    video_extensions = current_app.config.get('VIDEO_EXTENSIONS')
    # Securely resolve and join the target directory path
    target_dir = safe_join(video_dir, subpath)

    if not target_dir or not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        return jsonify({"error": "Folder not found"}), 404

    items = []

    try:
        for entry in os.scandir(target_dir):
            relative_item_path = os.path.relpath(entry.path, video_dir).replace("\\", "/")

            # check if it`s a directory
            if entry.is_dir():
                items.append({
                    "name": entry.name,
                    "type": "folder",
                    "path": relative_item_path
                })
            # check if it`s video file
            elif entry.is_file() and entry.name.lower().endswith(video_extensions):
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
@main_bp.route('/video-stream/<path:filepath>')
def video_stream(filepath):
    video_dir = current_app.config.get('VIDEO_DIR')
    return send_from_directory(video_dir, filepath)