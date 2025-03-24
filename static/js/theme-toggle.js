function setTheme(theme) {
    const link = document.getElementById('theme-stylesheet');
    link.href = `/static/css/${theme}.css`;
    localStorage.setItem('theme', theme);

    // Wait for CSS to load before showing the page
    link.onload = () => {
        document.body.style.display = 'block';
    };
}

function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'light';
    const nextTheme = currentTheme === 'light' ? 'dracula' : 'light';
    setTheme(nextTheme);
}

window.onload = () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
};
