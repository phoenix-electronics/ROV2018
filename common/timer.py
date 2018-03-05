from time import sleep, perf_counter


class Timer:
    """Class for tracking elapsed time"""

    def __init__(self, duration: float, start_expired: bool = False) -> None:
        self.duration = duration
        self.start_time = perf_counter()
        if start_expired:
            self.start_time -= self.duration

    def is_expired(self) -> bool:
        """Return whether the timer is expired"""
        return self.get_remaining_time() == 0

    def get_elapsed_time(self) -> float:
        """Return the elapsed time in seconds"""
        return perf_counter() - self.start_time

    def get_remaining_time(self) -> float:
        """Return the remaining time in seconds"""
        return max(self.duration - self.get_elapsed_time(), 0)

    def wait(self) -> None:
        """Block until the timer expires"""
        sleep(self.get_remaining_time())

    def restart(self) -> None:
        """Reset the timer"""
        self.start_time = perf_counter()
