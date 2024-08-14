document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('autoResizeTextarea');

    // Auto-resize the textarea
    if (textarea) {
        textarea.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});
