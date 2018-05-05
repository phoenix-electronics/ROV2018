from subprocess import Popen, DEVNULL


class SoundPlayer:
    def __init__(self) -> None:
        self._player_process = None

    def play(self, filename: str, volume: float = 1.0) -> None:
        """Stop the currently playing sound (if any), and play a new sound"""
        volume_millibels = int((volume - 1) * 6000)
        process_args = ['omxplayer.bin', '--no-keys', '--vol', str(volume_millibels), filename]
        self._player_process = Popen(process_args, stdout=DEVNULL, stderr=DEVNULL)

    def is_playing(self) -> bool:
        """Return whether a sound is currently playing"""
        return self._player_process is not None and self._player_process.poll() is None

    def stop(self) -> None:
        """Stop the sound that is currently playing, if any"""
        if self.is_playing():
            self._player_process.kill()
            self._player_process = None
