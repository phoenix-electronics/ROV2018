import pygame


class Widget:
    def __init__(self, pos: (int, int), size: (int, int), color=(255, 255, 255)) -> None:
        self.pos = pos
        self.size = size
        self.surface = pygame.Surface(size)
        self.color = color
        self.children = []

    def blit(self, surface: pygame.Surface) -> None:
        self.surface.fill((0, 0, 0))
        self.draw()

        for child in self.children:
            child.blit(child, self.surface)

        surface.blit(self.surface, self.pos)

    def draw(self) -> None:
        pass
