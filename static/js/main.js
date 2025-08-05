document.addEventListener('DOMContentLoaded', function() {
    // --- Upload form logic (remains unchanged) ---
    const uploadForm = document.getElementById('upload-form');
    const loader = document.getElementById('loader');
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            if (fileInput.files.length > 0) {
                uploadForm.style.display = 'none';
                loader.style.display = 'block';
            }
        });
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
                fileNameDisplay.style.color = '#e0e0e0';
            } else {
                fileNameDisplay.textContent = 'Choose a file...';
            }
        });
    }

    // SIMPLIFIED AND ROBUST: Logic for ALL collapsible sections
    const explanationToggles = document.querySelectorAll('.explanation-toggle');
    
    explanationToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            
            // This logic is more reliable and robust.
            if (content.style.maxHeight) {
                // If it's open, close it by setting maxHeight to null (or "0px").
                content.style.maxHeight = null;
            } else {
                // If it's closed, open it to its full scrollHeight.
                // The browser will correctly calculate scrollHeight including all content and CSS padding.
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });
});