// Professional Dark Mode System
(function() {
    // Check for saved preference or system preference
    const savedMode = localStorage.getItem('darkMode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDarkMode = savedMode !== null ? savedMode === 'true' : prefersDark;
    
    // Apply theme on page load
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    window.currentDarkMode = isDarkMode;
    updateIcon();
})();

// Update icon based on theme
function updateIcon() {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.classList.remove('bi-moon', 'bi-sun');
        icon.classList.add(window.currentDarkMode ? 'bi-sun' : 'bi-moon');
    }
}

// Toggle dark mode
function toggleDarkMode() {
    window.currentDarkMode = !window.currentDarkMode;
    
    if (window.currentDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    
    localStorage.setItem('darkMode', window.currentDarkMode);
    updateIcon();
}
