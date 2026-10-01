import os
import sys
from flask import Flask
from routes import main_bp


def create_app(folder_path):
    # Configure static and template paths for PyInstaller standalone executable
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS')
        template_folder = os.path.join(base_path, 'templates')
        static_folder = os.path.join(base_path, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    else:
        app = Flask(__name__)

    # Save configuration variables to the Flask application config
    app.config['VIDEO_DIR'] = folder_path
    app.config['VIDEO_EXTENSIONS'] = ('.mp4', '.mkv', '.avi', '.mov', '.webm')
    # Register blueprint with routes
    app.register_blueprint(main_bp)

    return app


def run_server(ip, port, folder_path):
    app = create_app(folder_path)
    app.run(host=ip, port=int(port), debug=False, use_reloader=False)

