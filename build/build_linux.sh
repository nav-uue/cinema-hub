#!/bin/bash

# Force script to exit immediately if any command returns a non-zero status
set -e

# ==========================================
# CONFIGURATION (Change these values)
# ==========================================
REPO_URL="https://github.com/nav-uue/cinema-hub.git"
TEMP_DIR="/tmp/cinema-hub"
OUTPUT_DIR="$HOME/Desktop/cinema-hub" # Target folder for the final binary
BINARY_NAME="cinema-hub"          # Output file name

echo "🚀 Starting the automated build process for Linux..."

# 1. Clean up and create necessary folders
echo "📁 Preparing directories..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
mkdir -p "$OUTPUT_DIR"

# 2. Clone the repository
echo "📥 Cloning project from repository..."
git clone "$REPO_URL" "$TEMP_DIR/source"
cd "$TEMP_DIR/source"

# =========================================================================
# CHANGE DIRECTORY TO PROJECT ROOT (Since script runs from cloned structure)
# =========================================================================
# We are currently in '$TEMP_DIR/source'. The files (main.py, static, etc.)
# are right here, because git clones the repository root.
# =========================================================================

# 3. Set up the virtual environment (venv)
echo "📦 Creating and activating Python virtual environment (venv)..."
python3 -m venv venv
source venv/bin/activate

# 4. Upgrade pip and install dependencies
echo "📥 Installing required packages..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found! Installing base packages..."
    pip install flask pyinstaller
fi

# Ensure pyinstaller is explicitly installed in the venv
pip install pyinstaller

# 5. Build the project using PyInstaller
echo "🛠️ Launching PyInstaller compilation process..."
# Note: Linux uses a COLON (:) as a separator for --add-data
pyinstaller --onefile --noconsole \
            --add-data "templates:templates" \
            --add-data "static:static" \
            --name "$BINARY_NAME" \
            main.py

# 6. Move the binary to the output folder
echo "📦 Moving the final binary file..."
if [ -f "dist/$BINARY_NAME" ]; then
    cp "dist/$BINARY_NAME" "$OUTPUT_DIR/"
    echo "✅ Binary successfully saved to: $OUTPUT_DIR/$BINARY_NAME"
else
    echo "❌ Error: Binary file was not found in the dist directory."
    exit 1
fi

# 7. Deactivate environment and clean up workspace trash
echo "🧹 Cleaning up temporary files and workspace..."
deactivate
rm -rf "$TEMP_DIR"

echo "🎉 Build completed successfully!"