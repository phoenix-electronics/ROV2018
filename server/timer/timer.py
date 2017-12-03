from pygame.time import get_ticks


class Timer:
    def __init__(self, lifetime: int):
        self.lifetime = lifetime
        self.init_time = get_ticks()

    def is_expired(self):
        return get_ticks() - self.init_time > self.lifetime

    def expire(self):
        self.init_time = get_ticks() - self.lifetime - 1

    def restart(self):
        self.init_time = get_ticks()
