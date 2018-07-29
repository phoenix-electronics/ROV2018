import pygame

from server.widget import VerticalLayoutWidget, Widget


class Window:
    def __init__(self) -> None:
        self.surface = None
        self.widgets = VerticalLayoutWidget((4, 4), children=[], name='root').get_name_dict()

    def show(self) -> None:
        """Show the window"""
        pygame.display.init()
        self.surface = pygame.display.set_mode((324, 768))
        self.update()

    def is_showing(self) -> bool:
        """Return whether the window is showing"""
        return self.surface is not None

    def update(self) -> None:
        """Update the contents of the window"""
        self.surface.fill(Widget.DEFAULT_BG_COLOR)
        self.widgets.get('root').blit(self.surface)
        pygame.display.flip()

    def hide(self) -> None:
        """Hide the window"""
        self.surface = None
        pygame.display.quit()
