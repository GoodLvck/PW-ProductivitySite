let player;
let playing = false;
let playerReady = false;

const musicButton = document.getElementById('musicButton');
const musicIcon = document.getElementById('musicIcon');

window.onYouTubeIframeAPIReady = function () {
    player = new YT.Player('youtube-player', {
        height: '0',
        width: '0',
        playerVars: {
            autoplay: 0,
            controls: 0,
            listType: 'playlist',
            list: 'PLbjHb9vCXJO43SN_ENu7smSQVUTafAZ81',
            loop: 1
        },
        events: {
            onReady: function(e) {
                playerReady = true;
                e.target.setVolume(60);
            },
            onError: function(e) {
                console.error('YT Error:', e.data);
            }
        }
    });
};

musicButton.addEventListener('click', () => {
    if (!playerReady) return;

    if (playing) {
        player.pauseVideo();
        musicIcon.classList.remove('fi-rc-volume');
        musicIcon.classList.add('fi-rc-volume-mute');
    } else {
        player.playVideo();
        musicIcon.classList.remove('fi-rc-volume-mute');
        musicIcon.classList.add('fi-rc-volume');
    }
    playing = !playing;
});
