import pygame


class Widget:
    DEFAULT_COLOR = (255, 255, 255)

    def __init__(self, pos: (int, int), size: (int, int), children: ['Widget'] = None) -> None:
        self.pos = pos
        self.size = size
        self.color = Widget.DEFAULT_COLOR
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.children = children or []

    def blit(self, surface: pygame.Surface) -> None:
        self.surface.fill((0, 0, 0, 0))
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
            widths, heights = zip(*[child.size for child in children])
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
            widths, heights = zip(*[child.size for child in children])
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
        width, height = self.size
        x_max, y_max = width - 1, height - 1
        border_points = [(x * x_max, y * y_max) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        for side, border in enumerate(self.border):
            if border:
                point1, point2 = border_points[side], border_points[(side + 1) % 4]
                pygame.draw.line(self.surface, self.color, point1, point2)
        if self.value is None:
            size = min(x_max, y_max)
            orig_x, orig_y = (x_max - size) // 2, (y_max - size) // 2
            pygame.draw.line(self.surface, self.color, (orig_x, orig_y), (orig_x + size, orig_y + size))
            pygame.draw.line(self.surface, self.color, (orig_x, orig_y + size), (orig_x + size, orig_y))


class VerticalBarWidget(Widget):
    MODE_NORMAL, MODE_CENTER, MODE_INVERT = range(3)

    def __init__(self, pos: (int, int), size: (int, int), mode: int = MODE_NORMAL, top_text: str = None,
                 bot_text: str = None) -> None:
        children = []
        if top_text:
            children.append(TextWidget((0, 0), top_text))
        self.bar = BarWidget((0, 0), size, (True, False, True, False))
        children.append(self.bar)
        if bot_text:
            children.append(TextWidget((0, 0), bot_text))
        parent = VerticalLayoutWidget((0, 0), children=children, spacing=0)
        self.mode, self.value = mode, None
        super().__init__(pos, parent.size, children=[parent])

    def draw(self):
        mode, raw_value = self.mode, self.value
        self.bar.value = raw_value
        if raw_value is not None:
            v_min, v_max = [(0, 1), (-1, 1), (-1, 0)][mode]
            value = max(v_min, min(v_max, raw_value))
            surface, color = self.surface, self.color
            width, height = self.bar.size
            x_max, y_max = width - 1, height - 1
            v_padding = 2
            rect_x = self.bar.pos[0]
            rect_y = [y_max, y_max // 2, 0][mode] + self.bar.pos[1]
            rect_w = width
            rect_h = int((y_max // (v_max - v_min) - 2 * v_padding) * abs(value))
            if value > 0:
                pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y - v_padding, rect_w, -rect_h + 1))
            elif value < 0:
                pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y + v_padding, rect_w, rect_h + 1))
            if mode == VerticalBarWidget.MODE_CENTER:
                pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y, width, 1))


class HorizontalBarWidget(Widget):
    MODE_NORMAL, MODE_CENTER, MODE_INVERT = range(3)

    def __init__(self, pos: (int, int), size: (int, int), mode: int = MODE_NORMAL, left_text: str = None,
                 right_text: str = None) -> None:
        children = []
        if left_text:
            children.append(TextWidget((0, 0), left_text))
        self.bar = BarWidget((0, 0), size, (False, True, False, True))
        children.append(self.bar)
        if right_text:
            children.append(TextWidget((0, 0), right_text))
        parent = HorizontalLayoutWidget((0, 0), children=children, spacing=2)
        self.mode, self.value = mode, None
        super().__init__(pos, parent.size, children=[parent])

    def draw(self) -> None:
        mode, raw_value = self.mode, self.value
        self.bar.value = raw_value
        if raw_value is not None:
            h_min, h_max = [(0, 1), (-1, 1), (-1, 0)][mode]
            value = max(h_min, min(h_max, raw_value))
            surface, color = self.surface, self.color
            width, height = self.bar.size
            x_max, y_max = width - 1, height - 1
            h_padding = 2
            rect_x = [0, x_max // 2, x_max][mode] + self.bar.pos[0]
            rect_y = self.bar.pos[1]
            rect_w = int((x_max // (h_max - h_min) - 2 * h_padding) * abs(value))
            rect_h = height
            if value > 0:
                pygame.draw.rect(surface, color, pygame.Rect(rect_x + h_padding, rect_y, rect_w + 1, rect_h))
            elif value < 0:
                pygame.draw.rect(surface, color, pygame.Rect(rect_x - h_padding, rect_y, -rect_w + 1, rect_h))
            if mode == VerticalBarWidget.MODE_CENTER:
                pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y, 1, height))
