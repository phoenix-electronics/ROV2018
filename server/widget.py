from typing import Tuple, List

import pygame


class Widget:
    DEFAULT_COLOR = (255, 255, 255)

    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], children: List['Widget'] = None) -> None:
        self.pos = pos
        self.size = size
        self.color = Widget.DEFAULT_COLOR
        self.visible = True
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.children = children if children else []

    def blit(self, surface: pygame.Surface) -> None:
        if self.visible:
            self.surface.fill((0, 0, 0, 0))
            self.draw()
            for child in self.children:
                child.blit(self.surface)
            surface.blit(self.surface, self.pos)

    def _scx(self, x: float, margin: int = 0) -> int:
        return int((self.size[0] - 1 - margin * 2) * x) + margin

    def _scy(self, y: float, margin: int = 0) -> int:
        return int((self.size[1] - 1 - margin * 2) * y) + margin

    def _sc(self, x: float, y: float, margin: int = 0) -> Tuple[int, int]:
        return self._scx(x, margin), self._scy(y, margin)

    def draw(self) -> None:
        pass


class VerticalLayoutWidget(Widget):
    ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT = range(3)

    def __init__(self, pos: Tuple[int, int], children: [Widget], alignment: int = ALIGN_CENTER,
                 spacing: int = 0) -> None:
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

    def __init__(self, pos: Tuple[int, int], children: [Widget], alignment: int = ALIGN_MIDDLE,
                 spacing: int = 0) -> None:
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
    def __init__(self, pos: Tuple[int, int], top: Widget = None, right: Widget = None, bottom: Widget = None,
                 left: Widget = None, center: Widget = None, spacing: int = 0) -> None:
        h_widget = HorizontalLayoutWidget((0, 0), list(filter(None, (left, center, right))), spacing=spacing)
        v_widget = VerticalLayoutWidget((0, 0), list(filter(None, (top, h_widget, bottom))), spacing=spacing)
        super().__init__(pos, v_widget.size, children=[v_widget])


class TextWidget(Widget):
    _loaded_fonts = {}

    def __init__(self, pos: Tuple[int, int], text: str, font_size: int = 15) -> None:
        if font_size not in self._loaded_fonts:
            self._loaded_fonts[font_size] = pygame.font.SysFont('Arial', font_size)
        self.font = self._loaded_fonts[font_size]
        self.text = text
        self._last_drawn_text = None
        self.text_surface = None
        super().__init__(pos, self.font.size(text))

    def draw(self) -> None:
        if self.text != self._last_drawn_text:
            self.text_surface = self.font.render(self.text, False, self.color)
            self._last_drawn_text = self.text
        self.surface.blit(self.text_surface, (0, 0))


class GlyphWidget(Widget):
    GLYPH_NONE, GLYPH_ERROR, GLYPH_SQUARE = range(3)

    def __init__(self, pos: Tuple[int, int], size: int, glyph: int, margin: int = 0) -> None:
        self.glyph = glyph
        self.margin = margin
        super().__init__(pos, (size, size))

    def draw(self) -> None:
        glyph, margin, surface, color = self.glyph, self.margin, self.surface, self.color
        if glyph == GlyphWidget.GLYPH_ERROR:
            pygame.draw.line(surface, color, self._sc(0, 0, margin), self._sc(1, 1, margin))
            pygame.draw.line(surface, color, self._sc(0, 1, margin), self._sc(1, 0, margin))
        elif glyph == GlyphWidget.GLYPH_SQUARE:
            dist, size = margin, self.size[0] - margin - 1
            pygame.draw.rect(surface, color, (dist, dist, size, size))


class BarWidget(Widget):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], border: Tuple[bool, bool, bool, bool]) -> None:
        self.border = border
        self.value = None
        glyph_size = min(*size)
        glyph_x, glyph_y = (size[0] - glyph_size) // 2, (size[1] - glyph_size) // 2
        self.glyph = GlyphWidget((glyph_x, glyph_y), glyph_size, GlyphWidget.GLYPH_ERROR)
        super().__init__(pos, size, [self.glyph])

    def draw(self) -> None:
        border_points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for side, border in enumerate(self.border):
            if border:
                line_start, line_end = border_points[side], border_points[(side + 1) % 4]
                pygame.draw.line(self.surface, self.color, self._sc(*line_start), self._sc(*line_end))
        self.glyph.visible = self.value is None


class VerticalBarWidget(Widget):
    MODE_NORMAL, MODE_CENTER, MODE_INVERT = range(3)

    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], mode: int = MODE_NORMAL, top_text: str = None,
                 bot_text: str = None, border: Tuple[bool, bool, bool, bool] = None) -> None:
        children = []
        if top_text:
            children.append(TextWidget((0, 0), top_text))
        self.bar = BarWidget((0, 0), size, border or (True, False, True, False))
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
                pygame.draw.rect(surface, color, (rect_x, rect_y - v_padding, rect_w, -rect_h + 1))
            elif value < 0:
                pygame.draw.rect(surface, color, (rect_x, rect_y + v_padding, rect_w, rect_h + 1))
            if mode == VerticalBarWidget.MODE_CENTER:
                pygame.draw.rect(surface, color, (rect_x, rect_y, width, 1))


class HorizontalBarWidget(Widget):
    MODE_NORMAL, MODE_CENTER, MODE_INVERT = range(3)

    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], mode: int = MODE_NORMAL, left_text: str = None,
                 right_text: str = None, border: Tuple[bool, bool, bool, bool] = None) -> None:
        children = []
        if left_text:
            children.append(TextWidget((0, 0), left_text))
        self.bar = BarWidget((0, 0), size, border or (False, True, False, True))
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
                pygame.draw.rect(surface, color, (rect_x + h_padding, rect_y, rect_w + 1, rect_h))
            elif value < 0:
                pygame.draw.rect(surface, color, (rect_x - h_padding, rect_y, -rect_w + 1, rect_h))
            if mode == VerticalBarWidget.MODE_CENTER:
                pygame.draw.rect(surface, color, (rect_x, rect_y, 1, height))


class LabeledContainerWidget(Widget):
    DEFAULT_LABEL_COLOR = (0, 0, 0)

    def __init__(self, pos: Tuple[int, int], child: Widget, text: str, padding: int = 4) -> None:
        self.label = TextWidget((5, 2), text, font_size=11)
        self.label.color = self.DEFAULT_LABEL_COLOR
        self.padding = padding
        label_w, label_h = self.label.size
        child_w, child_h = child.size
        child.pos = (padding, label_h + 4 + padding)
        width = max(label_w + 8, child_w + 2 * padding)
        height = label_h + 4 + child_h + 2 * padding
        super().__init__(pos, (width, height), children=[self.label, child])

    def draw(self) -> None:
        surface, color = self.surface, self.color
        label_w, label_h = self.label.size
        width, height = self.size
        pygame.draw.rect(surface, color, (0, 0, label_w + 8, label_h + 4))
        pygame.draw.rect(surface, color, (0, label_h + 4, width, height - label_h - 4), 1)
