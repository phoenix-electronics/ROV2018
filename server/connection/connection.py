import pygame


class Connection:
    DEFAULT_TTL = 100

    def __init__(self) -> None:
        self.ttl = self.DEFAULT_TTL
        self.init_time = 0
        self._open = False

    def open(self) -> None:
        self._open = True
        self.init_time = pygame.time.get_ticks()

    def close(self) -> None:
        self._open = False

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.init_time > self.ttl

    def is_open(self) -> bool:
        if self.is_expired():
            self.close()
        return self._open
