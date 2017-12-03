from server.timer.timer import Timer


class Connection:
    DEFAULT_TTL = 100

    def __init__(self, ttl: int = DEFAULT_TTL) -> None:
        self.timer = Timer(ttl)
        self._open = False

    def open(self) -> None:
        self._open = True
        self.timer.restart()

    def close(self) -> None:
        self._open = False

    def is_expired(self) -> bool:
        return self.timer.is_expired()

    def is_open(self) -> bool:
        if self.is_expired():
            self.close()
        return self._open
