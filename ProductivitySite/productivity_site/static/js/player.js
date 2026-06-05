let player = null;
let playerReady = false;
let autoplayBlocked = false;
let autoplayProbeTimer = null;

const musicButton = document.getElementById('musicButton');
const musicIcon = document.getElementById('musicIcon');
const musicLabel = document.getElementById('musicLabel');

const MUSIC_STATE_KEY = 'music';
const MUSIC_VOLUME_KEY = 'music_volume';
const DEFAULT_VOLUME = 70;

let playing = localStorage.getItem(MUSIC_STATE_KEY) === 'playing';
let volume = Number.parseInt(localStorage.getItem(MUSIC_VOLUME_KEY) || `${DEFAULT_VOLUME}`, 10);
if (Number.isNaN(volume) || volume < 0 || volume > 100) {
    volume = DEFAULT_VOLUME;
}

function setButtonState(state) {
    if (!musicButton) {
        return;
    }
    musicButton.classList.remove('is-loading', 'is-error');
    if (state) {
        musicButton.classList.add(state);
    }
}

function updateMusicUi() {
    if (!musicIcon || !musicLabel) {
        return;
    }
    if (!playerReady) {
        if (playing) {
            musicIcon.className = 'fi fi-rc-volume';
            musicLabel.textContent = 'Loading...';
            setButtonState('is-loading');
        } else {
            musicIcon.className = 'fi fi-rc-volume-mute';
            musicLabel.textContent = 'Lofi live';
        }
        return;
    }

    if (playing) {
        musicIcon.className = 'fi fi-rc-volume';
        musicLabel.textContent = 'Pause';
    } else {
        musicIcon.className = 'fi fi-rc-volume-mute';
        musicLabel.textContent = 'Lofi live';
    }
}

function applyPlaybackFromState() {
    if (!player || !playerReady) {
        return;
    }

    player.unMute();
    player.setVolume(volume);

    if (playing) {
        player.playVideo();
        if (autoplayProbeTimer) {
            window.clearTimeout(autoplayProbeTimer);
        }
        autoplayProbeTimer = window.setTimeout(() => {
            if (!player) {
                return;
            }
            const state = player.getPlayerState();
            if (state !== window.YT.PlayerState.PLAYING) {
                autoplayBlocked = true;
                playing = false;
                localStorage.setItem(MUSIC_STATE_KEY, 'paused');
                setButtonState('is-error');
                if (musicLabel) {
                    musicLabel.textContent = 'Autoplay block';
                }
            }
        }, 1800);
    } else {
        player.pauseVideo();
    }
}

function initYouTubePlayer() {
    if (!window.YT || !window.YT.Player) {
        return false;
    }
    player = new window.YT.Player('youtube-player', {
        height: '0',
        width: '0',
        videoId: 'jfKfPfyJRdk',
        playerVars: {
            autoplay: 0,
            controls: 0,
            listType: 'playlist',
            list: 'PLbjHb9vCXJO43SN_ENu7smSQVUTafAZ81',
            loop: 1
        },
        events: {
            onReady: function () {
                playerReady = true;
                setButtonState(null);
                applyPlaybackFromState();
                updateMusicUi();
            },
            onStateChange: function (event) {
                if (event.data === window.YT.PlayerState.PLAYING) {
                    autoplayBlocked = false;
                    playing = true;
                    localStorage.setItem(MUSIC_STATE_KEY, 'playing');
                    setButtonState(null);
                    updateMusicUi();
                }

                if (event.data === window.YT.PlayerState.PAUSED || event.data === window.YT.PlayerState.ENDED) {
                    playing = false;
                    localStorage.setItem(MUSIC_STATE_KEY, 'paused');
                    updateMusicUi();
                }
            },
            onError: function () {
                setButtonState('is-error');
                if (musicLabel) {
                    musicLabel.textContent = 'Audio error';
                }
            }
        },
    });

    return true;
}

function waitForYouTubeAndInit() {
    const maxTries = 100;
    let tries = 0;

    const timer = window.setInterval(() => {
        tries += 1;
        if (initYouTubePlayer()) {
            window.clearInterval(timer);
            return;
        }

        if (tries >= maxTries) {
            window.clearInterval(timer);
            setButtonState('is-error');
            if (musicLabel) {
                musicLabel.textContent = 'Not available';
            }
        }
    }, 100);
}

updateMusicUi();
if (playing) {
    setButtonState('is-loading');
}
waitForYouTubeAndInit();

if (musicButton) {
    musicButton.addEventListener('click', () => {
        if (!player || !playerReady) {
            setButtonState('is-loading');
            return;
        }

        if (playing) {
            player.pauseVideo();
            playing = false;
            localStorage.setItem(MUSIC_STATE_KEY, 'paused');
        } else {
            autoplayBlocked = false;
            setButtonState(null);
            player.unMute();
            player.setVolume(volume);
            player.playVideo();
            playing = true;
            localStorage.setItem(MUSIC_STATE_KEY, 'playing');
            updateMusicUi();
        }
        if (!playing) {
            updateMusicUi();
        }
    });
}
