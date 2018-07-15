import pygame


class Window:
    def __init__(self) -> None:
        self.surface = None

    def show(self) -> None:
        """Show the window"""
        pygame.display.init()
        self.surface = pygame.display.set_mode((324, 768))
        self.update()

    def is_showing(self) -> bool:
        return self.surface is not None

    def update(self) -> None:
        """Update the contents of the window"""
        self.surface.fill((0, 0, 0))
        pygame.display.flip()

    def hide(self) -> None:
        """Hide the window"""
        self.surface = None
        pygame.display.quit()
