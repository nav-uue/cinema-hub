# 🎬 "File Explorer" Style Movie Library on Flask

A lightweight Python (Flask) web application that scans a designated folder on your computer and displays video content using a **Windows File Explorer** interface style (specifically matching the "Large Icons" view).

## ✨ Features
* 📂 **Folder Navigation:** Seamlessly browse inside folders (TV shows/seasons) and navigate back using the "Up" button.
* 💻 **Simple design:** The interface completely mirrors the look and feel of the original Windows Explorer, including single-click item selection.
* 🎥 **Built-in Video Player:** Play video files (MP4, MKV, AVI, MOV, etc.) directly in a modern modal window on double-click without reloading the page.
* 🚀 **Clean Codebase:** Built using only Flask, Vanilla CSS, and native JavaScript — zero external CSS or JS libraries required.

---

## 📁 Project Structure

```text
├── app.py               # Server-side logic (Flask API, folder scanning, video streaming)
├── templates/
│   └── index.html       # HTML template for the Explorer interface
└── static/
    ├── css/
    │   └── style.css    # Interface layouts and custom CSS icons (Windows style)
    └── js/
        └── script.js    # Navigation logic, selection states, and API interaction
```

---

## 🚀 Quick Start Guide

### 1. Configure the Video Directory
Before running the server, open `app.py` and specify the absolute path to your media directory in the `VIDEO_DIR` variable:

```python
# Example for Linux / macOS
# VIDEO_DIR = "/home/your/directory/path"

# Example for Windows (the 'r' prefix is required for raw paths)
VIDEO_DIR = r"C:\your\directory\path"
```

### 2. Set Up Environment and Run

Install Flask and Werkzeug (if you haven't already), then launch the application server:

```bash
# Install required dependencies
pip install flask werkzeug

# Start the Flask development server
flask run --debug
```

### 3. Open in Browser
Open your favorite web browser and navigate to:
👉 **[URL](http://127.0.0.1:5000)**

---

## 📺 Streaming to Phone or TV (Local Network)

To watch your library on a smartphone, tablet, or Smart TV connected to the same home Wi-Fi network:

1. Find your computer's local IP address (e.g., `192.168.0.XX`).

   ```bash
   # Linux / macOS
   ifconfig

   # Windows
   ipconfig
   ```

2. Run the application with network access enabled (and debugger disabled for safety):

   ```bash
   python app.py
   ```

3. Open the browser on your phone or TV and type your IP followed by the port: `http://192.168.0.XX:5000`.

---

## 🛠️ Built With
* **Backend:** Python 3, Flask, Werkzeug
* **Frontend:** HTML5, CSS3 (Flexbox/Grid, CSS-based shapes), JavaScript (Async/Await Fetch API)
