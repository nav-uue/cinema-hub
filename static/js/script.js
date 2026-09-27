let currentPath = "";
let mouseTimer;
let currentFolderItems = []; // Храним файлы текущей папки глобально
let currentVideoIndex = -1;  // Индекс текущего видео в массиве видеофайлов

const grid = document.getElementById('filesGrid');
const pathDisplay = document.getElementById('pathDisplay');
const backBtn = document.getElementById('backBtn');
const modal = document.getElementById('videoModal');
const modalVideo = document.getElementById('modalVideo');
const modalTitle = document.getElementById('modalVideoTitle');
const closeBtn = document.getElementById('closeBtn');

const videoWrapper = document.getElementById('videoWrapper');
const prevVideoBtn = document.getElementById('prevVideoBtn');
const nextVideoBtn = document.getElementById('nextVideoBtn');

// Download files from server
async function loadFolder(path = "") {
    try {
        const response = await fetch(`/api/files/${path}`);
        if (!response.ok) throw new Error("Failed to load folder");

        const data = await response.json();
        currentPath = data.current_path;

        // Update navigation interface
        pathDisplay.textContent = currentPath ? `Storage > Video > ${currentPath.replace(/\//g, ' > ')}` : "Storage > Video";
        backBtn.disabled = currentPath === "";

        renderItems(data.items);
    } catch (error) {
        grid.innerHTML = `<div style="color:red; padding:20px;">Error: ${error.message}</div>`;
    }
}

// Render elements on the page
function renderItems(items) {
    grid.innerHTML = "";
    currentFolderItems = items;

    if (items.length === 0) {
        grid.innerHTML = '<div style="color:#666; padding:20px;">Folder is empty</div>';
        return;
    }

    items.forEach(item => {
        const fileItem = document.createElement('div');
        fileItem.className = `file-item ${item.type}`;

        fileItem.innerHTML = `
            <div class="icon-wrapper"></div>
            <div class="file-name">${item.name}</div>
        `;

        // Select file on click
        fileItem.addEventListener('click', (e) => {
            e.stopPropagation();
            document.querySelectorAll('.file-item').forEach(i => i.classList.remove('selected'));
            fileItem.classList.add('selected');
        });

        // Double click action
        fileItem.addEventListener('dblclick', () => {
            if (item.type === 'folder') {
                loadFolder(item.path); // Open folder
            } else if (item.type === 'video') {
                openVideo(item.url, item.name); // Open player
            }
        });

        grid.appendChild(fileItem);
    });
}

// Go to parent folder
backBtn.addEventListener('click', () => {
    if (!currentPath) return;
    const parts = currentPath.split('/');
    parts.pop(); // Remove the last folder from the path
    loadFolder(parts.join('/'));
});

// Clear selection if clicking on empty space
document.addEventListener('click', () => {
    document.querySelectorAll('.file-item').forEach(i => i.classList.remove('selected'));
});

/* --- MODAL PLAYER OPERATIONS--- */
// Hides the player interface (title and navigation buttons)
function hideTitle() {
    videoWrapper.classList.add('hide-ui');
}

// Shows the title and resets the inactivity timer
function resetTimer() {
    videoWrapper.classList.remove('hide-ui');
    clearTimeout(mouseTimer);
    // Hide the title after 2 seconds of mouse inactivity
    mouseTimer = setTimeout(hideTitle, 2000);
}

function openVideo(url, name) {
    // Filter the array to keep only video files
    const videoFiles = currentFolderItems.filter(item => item.type === 'video');
    // Find the index of the selected video by its URL or name
    currentVideoIndex = videoFiles.findIndex(item => item.url === url);

    modalVideo.src = url;
    modalTitle.textContent = name;
    modal.style.display = 'flex';

    updateNavButtons(); // Check navigation button states on open
    resetTimer();
}

function closeModal() {
    modal.style.display = 'none';
    modalVideo.pause();
    modalVideo.src = "";
    modalTitle.textContent = "";
    currentVideoIndex = -1; // Reset current index on close

    // Clear timer to avoid background execution
    clearTimeout(mouseTimer);
    videoWrapper.classList.remove('hide-ui');
}

// Enables or disables "Next" and "Previous" buttons
function updateNavButtons() {
    // Get only video files from the current folder
    const videoFiles = currentFolderItems.filter(item => item.type === 'video');
    // Disable "Previous" button if it`s the first video
    prevVideoBtn.disabled = (currentVideoIndex <= 0);
    // Disable "Next" button if it`s the last video
    nextVideoBtn.disabled = (currentVideoIndex >= videoFiles.length - 1 || currentVideoIndex === -1);
}

// Function to switch between videos
function changeVideo(direction) {
    const videoFiles = currentFolderItems.filter(item => item.type === 'video');

    // Calculate the new index
    const newIndex = currentVideoIndex + direction;

    // Check if the video exists at that index
    if (newIndex >= 0 && newIndex < videoFiles.length) {
        currentVideoIndex = newIndex;
        const nextVideo = videoFiles[currentVideoIndex];

        // Load the new video into the player
        modalVideo.src = nextVideo.url;
        modalTitle.textContent = nextVideo.name;
        modalVideo.play();

        updateNavButtons();
        resetTimer();
    }
}

// Track mouse movement over the player
videoWrapper.addEventListener('mousemove', resetTimer);

// If paused, show the title and keep it visible
modalVideo.addEventListener('pause', () => {
    videoWrapper.classList.remove('hide-ui');
    clearTimeout(mouseTimer);
});

// On video play, enable the autohide timer again
modalVideo.addEventListener('play', resetTimer);

// Add click event listeners to navigation buttons
prevVideoBtn.addEventListener('click', (e) => { e.stopPropagation(); changeVideo(-1); });
nextVideoBtn.addEventListener('click', (e) => { e.stopPropagation(); changeVideo(1); });

closeBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

// First run of program
loadFolder();
