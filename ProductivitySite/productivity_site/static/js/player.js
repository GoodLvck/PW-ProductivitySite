(function () {
    if (window.zenOrbitMusicInitialized) {
        window.zenOrbitMusic?.syncUi?.();
        return;
    }
    window.zenOrbitMusicInitialized = true;

    const MUSIC_STATE_KEY = 'music';
    const MUSIC_VOLUME_KEY = 'music_volume';
    const DEFAULT_VOLUME = 70;
    const STREAM_URL = 'https://dc1.serverse.com/proxy/dnutqhxl/stream';

    const parsedVolume = Number.parseInt(
        localStorage.getItem(MUSIC_VOLUME_KEY) || `${DEFAULT_VOLUME}`,
        10
    );

    const state = (window.zenOrbitMusic = {
        audio: null,
        playing: false,
        volume: Number.isNaN(parsedVolume) || parsedVolume < 0 || parsedVolume > 100
            ? DEFAULT_VOLUME
            : parsedVolume,
    });

    function getMusicElements() {
        return {
            musicButton: document.getElementById('musicButton'),
            musicIcon: document.getElementById('musicIcon'),
            musicLabel: document.getElementById('musicLabel'),
            musicShell: document.getElementById('music-player-shell'),
        };
    }

    function setButtonState(buttonState) {
        const { musicButton } = getMusicElements();
        if (!musicButton) {
            return;
        }

        musicButton.classList.remove('is-loading', 'is-error');
        if (buttonState) {
            musicButton.classList.add(buttonState);
        }
    }

    function ensureAudio() {
        const { musicShell } = getMusicElements();
        if (!musicShell) {
            return null;
        }

        if (!state.audio) {
            const audio = document.createElement('audio');
            audio.id = 'lofi-audio-player';
            audio.preload = 'none';
            audio.src = STREAM_URL;
            audio.volume = state.volume / 100;

            audio.addEventListener('playing', () => {
                state.playing = true;
                localStorage.setItem(MUSIC_STATE_KEY, 'playing');
                syncMusicUi();
            });

            audio.addEventListener('pause', () => {
                state.playing = false;
                localStorage.setItem(MUSIC_STATE_KEY, 'paused');
                syncMusicUi();
            });

            audio.addEventListener('error', () => {
                state.playing = false;
                setButtonState('is-error');
                const { musicLabel } = getMusicElements();
                if (musicLabel) {
                    musicLabel.textContent = 'Audio error';
                }
            });

            musicShell.replaceChildren(audio);
            state.audio = audio;
        }

        return state.audio;
    }

    function syncMusicUi() {
        const { musicButton, musicIcon, musicLabel } = getMusicElements();
        if (!musicIcon || !musicLabel) {
            return;
        }

        if (musicButton) {
            musicButton.setAttribute('aria-pressed', state.playing ? 'true' : 'false');
        }

        if (state.playing) {
            setButtonState(null);
            musicIcon.className = 'fi fi-rc-volume';
            musicLabel.textContent = 'Pause';
        } else {
            musicIcon.className = 'fi fi-rc-volume-mute';
            musicLabel.textContent = 'Lofi live';
        }
    }

    async function playMusic() {
        const audio = ensureAudio();
        if (!audio) {
            return;
        }

        setButtonState('is-loading');
        audio.volume = state.volume / 100;
        audio.src = STREAM_URL;

        try {
            await audio.play();
            state.playing = true;
            localStorage.setItem(MUSIC_STATE_KEY, 'playing');
            syncMusicUi();
        } catch (error) {
            state.playing = false;
            setButtonState('is-error');
            const { musicLabel } = getMusicElements();
            if (musicLabel) {
                musicLabel.textContent = 'Audio blocked';
            }
        }
    }

    function pauseMusic() {
        const audio = ensureAudio();
        if (audio) {
            audio.pause();
        }

        state.playing = false;
        localStorage.setItem(MUSIC_STATE_KEY, 'paused');
        syncMusicUi();
    }

    function toggleMusic() {
        if (state.playing) {
            pauseMusic();
            return;
        }

        playMusic();
    }

    window.initZenOrbitMusicPlayer = ensureAudio;
    state.syncUi = syncMusicUi;

    document.addEventListener('click', (event) => {
        const musicButton = event.target.closest('#musicButton');
        if (!musicButton) {
            return;
        }
        toggleMusic();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') {
            return;
        }

        const musicButton = event.target.closest('#musicButton');
        if (!musicButton) {
            return;
        }

        event.preventDefault();
        toggleMusic();
    });

    document.addEventListener('turbo:load', syncMusicUi);

    ensureAudio();
    syncMusicUi();
})();
