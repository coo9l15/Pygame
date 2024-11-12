document.addEventListener('DOMContentLoaded', () => {
    const downloadLinks = {
        Windows: 'docs/flappy_bird_windows.zip',
        Mac: 'exe/MacFlappyBird/',
        Linux: 'docs/flappy_bird_linux.zip'
    };

    document.getElementById('Windows').addEventListener('click', () => {
        window.location.href = downloadLinks.Windows;
    });

    document.getElementById('Mac').addEventListener('click', () => {
        window.location.href = downloadLinks.Mac;
    });

    document.getElementById('Linux').addEventListener('click', () => {
        window.location.href = downloadLinks.Linux;
    });
});
