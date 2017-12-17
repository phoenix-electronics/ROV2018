from time import sleep, perf_counter


class Timer:
    def __init__(self, length: float, start_expired: bool = False) -> None:
        self.length = length
        self.start_time = perf_counter()
        if start_expired:
            self.start_time -= self.length

    def is_expired(self) -> bool:
        return self.get_remaining_time() == 0

    def get_elapsed_time(self) -> float:
        return perf_counter() - self.start_time

    def get_remaining_time(self) -> float:
        return max(self.length - self.get_elapsed_time(), 0)

    def wait(self) -> None:
        sleep(self.get_remaining_time())

    def restart(self) -> None:
        self.start_time = perf_counter()
