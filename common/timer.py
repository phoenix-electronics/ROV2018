from time import sleep, perf_counter


class Timer:
    def __init__(self, length: float) -> None:
        self.length = length
        self.start_time = perf_counter()

    def is_expired(self) -> bool:
        return self.get_remaining_time() > 0

    def get_remaining_time(self) -> int:
        return max(perf_counter() - self.start_time, 0)

    def wait(self) -> None:
        sleep(self.get_remaining_time())

    def restart(self) -> None:
        self.start_time = perf_counter()
