from time import perf_counter


class Timer:
    def __init__(self, length: float):
        self.length = length
        self.start_time = perf_counter()

    def is_expired(self):
        return perf_counter() - self.start_time > self.length

    def restart(self):
        self.start_time = perf_counter()
