const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const themeLabel = document.getElementById('theme-label');

let dark = localStorage.getItem('theme') === 'dark';

// Estado inicial
function updateThemeUI() {
    if (dark) {
        themeIcon.className = 'fi fi-rc-sun';
        themeLabel.textContent = 'Light theme';
    } else {
        themeIcon.className = 'fi fi-rc-moon';
        themeLabel.textContent = 'Dark theme';
    }
}

updateThemeUI();

// Toggle
themeToggle.addEventListener('click', () => {
    dark = !dark;

    if (dark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    }

    updateThemeUI();
});