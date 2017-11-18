import pygame


class Widget:
    DEFAULT_COLOR = (255, 255, 255)

    def __init__(self, pos: (int, int), size: (int, int), children: ['Widget'] = None) -> None:
        self.pos = pos
        self.size = size
        self.color = Widget.DEFAULT_COLOR
        self.surface = pygame.Surface(size)
        self.children = children or []

    def blit(self, surface: pygame.Surface) -> None:
        self.surface.fill((0, 0, 0))
        self.draw()
        for child in self.children:
            child.blit(self.surface)
        surface.blit(self.surface, self.pos)

    def draw(self) -> None:
        pass


class VerticalLayoutWidget(Widget):
    ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT = range(3)

    def __init__(self, pos: (int, int), children: [Widget], alignment: int = ALIGN_CENTER, spacing: int = 0) -> None:
        width, height = 0, 0
        if children:
            (widths, heights) = zip(*[child.size for child in children])
            width, height = max(widths), sum(heights) + spacing * (len(children) - 1)
            y_offset = 0
            for index, child in enumerate(children):
                x_offset = [0, (width - widths[index]) // 2, width - widths[index]][alignment]
                child.pos = (x_offset, y_offset)
                y_offset += heights[index] + spacing
        super().__init__(pos, (width, height), children=children)


class HorizontalLayoutWidget(Widget):
    ALIGN_TOP, ALIGN_MIDDLE, ALIGN_BOTTOM = range(3)

    def __init__(self, pos: (int, int), children: [Widget], alignment: int = ALIGN_MIDDLE, spacing: int = 0) -> None:
        width, height = 0, 0
        if children:
            (widths, heights) = zip(*[child.size for child in children])
            width, height = sum(widths) + spacing * (len(children) - 1), max(heights)
            x_offset = 0
            for index, child in enumerate(children):
                y_offset = [0, (height - heights[index]) // 2, height - heights[index]][alignment]
                child.pos = (x_offset, y_offset)
                x_offset += widths[index] + spacing
        super().__init__(pos, (width, height), children=children)


class BorderLayoutWidget(Widget):
    def __init__(self, pos: (int, int), top: Widget = None, right: Widget = None, bottom: Widget = None,
                 left: Widget = None, center: Widget = None, spacing: int = 0) -> None:
        h_widget = HorizontalLayoutWidget((0, 0), list(filter(None, (left, center, right))), spacing=spacing)
        v_widget = VerticalLayoutWidget((0, 0), list(filter(None, (top, h_widget, bottom))), spacing=spacing)
        super().__init__(pos, v_widget.size, children=[v_widget])


class TextWidget(Widget):
    def __init__(self, pos: (int, int), text: str, font_size: int = 14, size: (int, int) = None) -> None:
        self.font = pygame.font.SysFont('Arial', font_size)
        self.text = text
        super().__init__(pos, size or self.font.size(text))

    def draw(self) -> None:
        text_surface = self.font.render(self.text, False, self.color)
        self.surface.blit(text_surface, (0, 0))


class BarWidget(Widget):
    def __init__(self, pos: (int, int), size: (int, int), border: (bool, bool, bool, bool)) -> None:
        self.border = border
        self.value = None
        super().__init__(pos, size)

    def draw(self) -> None:
        (width, height) = self.size
        border_points = [(x * (width - 1), y * (height - 1)) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        for side, border in enumerate(self.border):
            if border:
                point1, point2 = border_points[side], border_points[(side + 1) % 4]
                pygame.draw.line(self.surface, Widget.DEFAULT_COLOR, point1, point2)
        if self.value is None:
            size = min(width, height) - 1
            orig_x, orig_y = ((width - 1 - size) // 2), ((height - 1 - size) // 2)
            pygame.draw.line(self.surface, Widget.DEFAULT_COLOR, (orig_x, orig_y), (orig_x + size, orig_y + size))
            pygame.draw.line(self.surface, Widget.DEFAULT_COLOR, (orig_x, orig_y + size), (orig_x + size, orig_y))
