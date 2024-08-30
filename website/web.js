document.addEventListener('DOMContentLoaded', (event) => {
    const downloadLinks = {
        Windows: '/path/to/flappy_bird_windows.zip',
        Mac: '/Users/Avee/Documents/Pygame/flappy_bird/images/try_again_button.png',
        Linux: '/path/to/flappy_bird_linux.zip'
    };

    function initiateDownload(os) {
        const link = document.createElement('a');
        link.href = downloadLinks[os];
        link.download = `flappy_bird_${os.toLowerCase()}.zip`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    Object.keys(downloadLinks).forEach(os => {
        const button = document.getElementById(os);
        button.addEventListener('click', () => initiateDownload(os));
    });
});