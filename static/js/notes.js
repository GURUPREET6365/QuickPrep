// notes.js - Drag & Drop and File Handling

// File validation constants
const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20MB in bytes
const ALLOWED_TYPES = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
const ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png'];

// DataTransfer object to hold selected files
let selectedFiles = new DataTransfer();

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const hiddenFileInput = document.getElementById('hiddenFileInput');
const selectedFilesContainer = document.getElementById('selectedFilesContainer');
const filesList = document.getElementById('filesList');
const fileCount = document.getElementById('fileCount');
const clearAllBtn = document.getElementById('clearAllBtn');
const uploadForm = document.getElementById('uploadForm');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeDropZone();
    initializeFileInput();
    initializeClearButton();
    initializeUploadForm();
});

// Initialize drag and drop functionality
function initializeDropZone() {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    // Handle click to open file browser
    dropZone.addEventListener('click', function() {
        fileInput.click();
    });
}

// Initialize file input change event
function initializeFileInput() {
    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
        // Reset input so the same file can be selected again
        e.target.value = '';
    });
}

// Initialize clear all button
function initializeClearButton() {
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            clearAllFiles();
        });
    }
}

// Initialize upload form
function initializeUploadForm() {
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (selectedFiles.files.length === 0) {
                e.preventDefault();
                alert('Please select at least one file to upload.');
                return false;
            }
            
            // Show loading state
            const uploadBtn = document.getElementById('uploadBtn');
            if (uploadBtn) {
                uploadBtn.disabled = true;
                uploadBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i> Uploading...';
            }
        });
    }
}

// Prevent default drag behaviors
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop zone
function highlight(e) {
    dropZone.style.borderColor = 'rgba(56,189,248,0.6)';
    dropZone.style.background = 'rgba(56,189,248,0.1)';
    dropZone.style.transform = 'scale(1.02)';
}

// Remove highlight from drop zone
function unhighlight(e) {
    dropZone.style.borderColor = 'rgba(56,189,248,0.3)';
    dropZone.style.background = 'rgba(56,189,248,0.03)';
    dropZone.style.transform = 'scale(1)';
}

// Handle dropped files
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// Handle selected files
function handleFiles(files) {
    if (files.length === 0) return;

    let validFiles = [];
    let errors = [];

    // Validate each file
    Array.from(files).forEach(file => {
        const validation = validateFile(file);
        if (validation.valid) {
            validFiles.push(file);
        } else {
            errors.push(`${file.name}: ${validation.error}`);
        }
    });

    // Show errors if any
    if (errors.length > 0) {
        alert('Some files were not added:\n\n' + errors.join('\n'));
    }

    // Add valid files to selection
    if (validFiles.length > 0) {
        validFiles.forEach(file => {
            selectedFiles.items.add(file);
        });
        updateFilesList();
        showSelectedFilesContainer();
    }
}

// Validate individual file
function validateFile(file) {
    // Check file size
    if (file.size > MAX_FILE_SIZE) {
        return {
            valid: false,
            error: 'File size exceeds 20MB'
        };
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
        return {
            valid: false,
            error: 'Only PDF, JPG, JPEG, PNG files are allowed'
        };
    }

    // Check MIME type if available
    if (file.type && !ALLOWED_TYPES.includes(file.type)) {
        return {
            valid: false,
            error: 'Invalid file type'
        };
    }

    return { valid: true };
}

// Update files list display
function updateFilesList() {
    filesList.innerHTML = '';
    fileCount.textContent = selectedFiles.files.length;

    Array.from(selectedFiles.files).forEach((file, index) => {
        const fileItem = createFileItem(file, index);
        filesList.appendChild(fileItem);
    });

    // Update hidden input
    hiddenFileInput.files = selectedFiles.files;
}

// Create file item element
function createFileItem(file, index) {
    const div = document.createElement('div');
    div.style.cssText = `
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem;
        background: rgba(56,189,248,0.05);
        border: 1px solid rgba(56,189,248,0.15);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    `;

    // File icon based on type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    let iconClass = 'bi-file-earmark-fill';
    let iconColor = '#22c55e';

    if (fileExtension === 'pdf') {
        iconClass = 'bi-file-earmark-pdf-fill';
        iconColor = '#ef4444';
    } else if (['jpg', 'jpeg', 'png'].includes(fileExtension)) {
        iconClass = 'bi-file-earmark-image-fill';
        iconColor = '#a855f7';
    }

    div.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem; flex: 1; min-width: 0;">
            <i class="bi ${iconClass}" style="font-size: 1.5rem; color: ${iconColor}; flex-shrink: 0;"></i>
            <div style="min-width: 0; flex: 1;">
                <div style="color: #cbd5e1; font-weight: 500; font-size: 0.875rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${file.name}">
                    ${file.name}
                </div>
                <div style="color: #64748b; font-size: 0.75rem;">
                    ${formatFileSize(file.size)}
                </div>
            </div>
        </div>
        <button type="button" 
                class="remove-file-btn"
                data-index="${index}"
                style="background: rgba(239,68,68,0.1);
                       border: 1px solid #ef4444;
                       color: #ef4444;
                       padding: 0.25rem 0.5rem;
                       border-radius: 6px;
                       font-size: 0.75rem;
                       cursor: pointer;
                       transition: all 0.2s ease;
                       flex-shrink: 0;"
                onmouseover="this.style.background='rgba(239,68,68,0.2)'"
                onmouseout="this.style.background='rgba(239,68,68,0.1)'">
            <i class="bi bi-x-lg"></i>
        </button>
    `;

    // Add remove button event listener
    const removeBtn = div.querySelector('.remove-file-btn');
    removeBtn.addEventListener('click', function() {
        removeFile(index);
    });

    // Hover effect
    div.addEventListener('mouseenter', function() {
        this.style.background = 'rgba(56,189,248,0.1)';
        this.style.borderColor = 'rgba(56,189,248,0.3)';
    });
    div.addEventListener('mouseleave', function() {
        this.style.background = 'rgba(56,189,248,0.05)';
        this.style.borderColor = 'rgba(56,189,248,0.15)';
    });

    return div;
}

// Remove file from selection
function removeFile(index) {
    const newDataTransfer = new DataTransfer();
    
    Array.from(selectedFiles.files).forEach((file, i) => {
        if (i !== index) {
            newDataTransfer.items.add(file);
        }
    });
    
    selectedFiles = newDataTransfer;
    
    if (selectedFiles.files.length === 0) {
        hideSelectedFilesContainer();
    } else {
        updateFilesList();
    }
}

// Clear all files
function clearAllFiles() {
    selectedFiles = new DataTransfer();
    hideSelectedFilesContainer();
}

// Show selected files container
function showSelectedFilesContainer() {
    if (selectedFilesContainer) {
        selectedFilesContainer.style.display = 'block';
        // Smooth scroll to selected files
        selectedFilesContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Hide selected files container
function hideSelectedFilesContainer() {
    if (selectedFilesContainer) {
        selectedFilesContainer.style.display = 'none';
    }
    filesList.innerHTML = '';
    fileCount.textContent = '0';
}

// Format file size for display
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Handle window paste event for quick file upload
document.addEventListener('paste', function(e) {
    const items = e.clipboardData?.items;
    if (!items) return;

    const files = [];
    for (let i = 0; i < items.length; i++) {
        if (items[i].kind === 'file') {
            const file = items[i].getAsFile();
            if (file) files.push(file);
        }
    }

    if (files.length > 0) {
        handleFiles(files);
    }
});

console.log('✅ Notes.js loaded successfully - Drag & Drop and File Upload enabled');