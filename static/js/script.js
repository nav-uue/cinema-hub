let currentPath = "";

const grid = document.getElementById('filesGrid');
const pathDisplay = document.getElementById('pathDisplay');
const backBtn = document.getElementById('backBtn');
const modal = document.getElementById('videoModal');
const modalVideo = document.getElementById('modalVideo');
const modalTitle = document.getElementById('modalVideoTitle');
const closeBtn = document.getElementById('closeBtn');

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

// Modal player operations
function openVideo(url, name) {
    modalVideo.src = url;
    modalTitle.textContent = name;
    modal.style.display = 'flex';
}

function closeModal() {
    modal.style.display = 'none';
    modalVideo.pause();
    modalVideo.src = "";
}

closeBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

// First run of program
loadFolder();
