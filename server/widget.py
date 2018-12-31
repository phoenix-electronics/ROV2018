from math import ceil
from typing import Dict, List, Tuple

import pygame

Vec2D = Tuple[int, int]

"""Widgets are UI elements that can be rendered to a PyGame Surface"""


class Widget:
    """Base widget class"""

    DEFAULT_FG_COLOR = (255, 255, 255)
    DEFAULT_BG_COLOR = (0, 0, 0)

    def __init__(self, pos: Vec2D, size: Vec2D, children: List['Widget'] = None, name: str = None) -> None:
        self.pos = pos
        self.size = size
        self.children = children if children is not None else []
        self.name = name

        self.color = self.DEFAULT_FG_COLOR
        self.visible = True
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

    def blit(self, surface: pygame.Surface) -> None:
        """Recursively draw the widget and its children, and blit the result onto the provided surface"""
        if self.visible:
            self.surface.fill((0, 0, 0, 0))
            self.draw()
            for child in self.children:
                child.blit(self.surface)
            surface.blit(self.surface, self.pos)

    def get_name_dict(self) -> Dict[str, 'Widget']:
        """Recursively search for named widgets, returning a dictionary indexed by name"""
        name_dict = {}
        if self.name:
            name_dict[self.name] = self
        for child in self.children:
            name_dict.update(child.get_name_dict())
        return name_dict

    def _scx(self, x: float, margin: int = 0) -> int:
        return int((self.size[0] - 1 - margin * 2) * x) + margin

    def _scy(self, y: float, margin: int = 0) -> int:
        return int((self.size[1] - 1 - margin * 2) * y) + margin

    def _sc(self, x: float, y: float, margin: int = 0) -> Vec2D:
        return self._scx(x, margin), self._scy(y, margin)

    def draw(self) -> None:
        """Draw the widget onto its surface"""
        pass


class VerticalLayoutWidget(Widget):
    """Widget that lays out its children in a single vertical row"""

    ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT = range(3)

    def __init__(self, pos: Vec2D, children: [Widget], alignment: int = ALIGN_LEFT, spacing: int = 4,
                 name: str = None) -> None:
        width, height = 0, 0
        if children:
            widths, heights = zip(*[child.size for child in children])
            width, height = max(widths), sum(heights) + spacing * (len(children) - 1)
            y_offset = 0
            for index, child in enumerate(children):
                x_offset = [0, (width - widths[index]) // 2, width - widths[index]][alignment]
                child.pos = (x_offset, y_offset)
                y_offset += heights[index] + spacing
        super().__init__(pos, (width, height), children=children, name=name)


class HorizontalLayoutWidget(Widget):
    """Widget that lays out its children in a single horizontal row"""

    ALIGN_TOP, ALIGN_MIDDLE, ALIGN_BOTTOM = range(3)

    def __init__(self, pos: Vec2D, children: [Widget], alignment: int = ALIGN_TOP, spacing: int = 4,
                 name: str = None) -> None:
        width, height = 0, 0
        if children:
            widths, heights = zip(*[child.size for child in children])
            width, height = sum(widths) + spacing * (len(children) - 1), max(heights)
            x_offset = 0
            for index, child in enumerate(children):
                y_offset = [0, (height - heights[index]) // 2, height - heights[index]][alignment]
                child.pos = (x_offset, y_offset)
                x_offset += widths[index] + spacing
        super().__init__(pos, (width, height), children=children, name=name)


class BorderLayoutWidget(Widget):
    """Widget that lays out its children in top, left, right, bottom, and center positions"""

    def __init__(self, pos: Vec2D, top: Widget = None, right: Widget = None, bottom: Widget = None, left: Widget = None,
                 center: Widget = None, spacing: int = 4, name: str = None) -> None:
        h_widget = HorizontalLayoutWidget((0, 0), list(filter(None, (left, center, right))),
                                          alignment=HorizontalLayoutWidget.ALIGN_MIDDLE, spacing=spacing)
        v_widget = VerticalLayoutWidget((0, 0), list(filter(None, (top, h_widget, bottom))),
                                        alignment=VerticalLayoutWidget.ALIGN_CENTER, spacing=spacing)
        super().__init__(pos, v_widget.size, children=[v_widget], name=name)


class TextWidget(Widget):
    """Widget that displays text"""

    FONT_SM = ('Roboto Mono Medium', 11)
    FONT_MD = ('Roboto Mono Medium', 13)
    FONT_LG = ('Roboto Mono Medium', 15)

    _loaded_fonts = {}

    def __init__(self, pos: Vec2D, text: str, font: Tuple[str, int] = FONT_MD, name: str = None) -> None:
        if font not in self._loaded_fonts:
            self._loaded_fonts[font] = pygame.font.SysFont(*font)
        self.font = self._loaded_fonts[font]
        self.text = text
        self._text = None
        self.text_surface = None
        super().__init__(pos, self.font.size(text), name=name)

    def draw(self) -> None:
        if self.text != self._text:
            self.text_surface = self.font.render(self.text, True, self.color)
            self._text = self.text
        self.surface.blit(self.text_surface, (0, 0))


class GlyphWidget(Widget):
    """Widget that displays a glyph"""

    GLYPH_NONE, GLYPH_ERROR, GLYPH_SQUARE = range(3)

    def __init__(self, pos: Vec2D, size: int, glyph: int, margin: int = 0, name: str = None) -> None:
        self.glyph = glyph
        self.margin = margin
        super().__init__(pos, (size, size), name=name)

    def draw(self) -> None:
        glyph, margin, surface, color = self.glyph, self.margin, self.surface, self.color
        if glyph == GlyphWidget.GLYPH_ERROR:
            pygame.draw.line(surface, color, self._sc(0, 0, margin), self._sc(1, 1, margin))
            pygame.draw.line(surface, color, self._sc(0, 1, margin), self._sc(1, 0, margin))
        elif glyph == GlyphWidget.GLYPH_SQUARE:
            dist, size = margin, self.size[0] - margin * 2
            pygame.draw.rect(surface, color, (dist, dist, size, size))


class BarWidget(Widget):
    """Widget that displays a fillable bar with optional borders and margin"""

    FROM_TOP, FROM_RIGHT, FROM_BOTTOM, FROM_LEFT = range(4)

    def __init__(self, pos: Vec2D, size: Vec2D, direction: int = FROM_LEFT,
                 border: Tuple[bool, bool, bool, bool] = None, margin: int = 2, name: str = None) -> None:
        self.direction = direction
        self.border = [(True, False) * 2, (False, True) * 2][direction % 2] if border is None else border
        self.margin = tuple([int(b) * margin for b in self.border])
        self.value = None
        glyph_size = min(*size)
        glyph_x, glyph_y = (size[0] - glyph_size) // 2, (size[1] - glyph_size) // 2
        self.glyph = GlyphWidget((glyph_x, glyph_y), glyph_size, GlyphWidget.GLYPH_ERROR)
        super().__init__(pos, size, [self.glyph], name=name)

    def draw(self) -> None:
        surface, color, direction, margin, value = self.surface, self.color, self.direction, self.margin, self.value
        width, height = self.size
        border_points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for side, border in enumerate(self.border):
            if border:
                line_start, line_end = border_points[side], border_points[(side + 1) % 4]
                pygame.draw.line(self.surface, self.color, self._sc(*line_start), self._sc(*line_end))
        if self.value:
            max_bar_w = (width - margin[1] - margin[3])
            max_bar_h = (height - margin[0] - margin[2])
            x = int(margin[3] + ((1 - value) * max_bar_w if direction == self.FROM_RIGHT else 0))
            y = int(margin[0] + ((1 - value) * max_bar_h if direction == self.FROM_BOTTOM else 0))
            w = ceil(value * max_bar_w if direction == self.FROM_LEFT else width - margin[1] - x)
            h = ceil(value * max_bar_h if direction == self.FROM_TOP else height - margin[0] - y)
            pygame.draw.rect(surface, color, (x, y, w, h))
        self.glyph.visible = self.value is None


class LabeledContainerWidget(Widget):
    """Widget that displays a child widget with a title bar"""

    def __init__(self, pos: Vec2D, width: int, child: Widget, text: str, padding: int = 4, name: str = None) -> None:
        self.label = TextWidget((5, 2), text, TextWidget.FONT_SM)
        self.label.color = self.DEFAULT_BG_COLOR
        self.padding = padding
        child.pos = (padding, self.label.size[1] + 4 + padding)
        height = self.label.size[1] + 4 + child.size[1] + 2 * padding
        super().__init__(pos, (width, height), children=[self.label, child], name=name)

    def draw(self) -> None:
        surface, color = self.surface, self.color
        label_height = self.label.size[1]
        width, height = self.size
        pygame.draw.rect(surface, color, (0, 0, width, label_height + 4))
        pygame.draw.rect(surface, color, (0, label_height + 4, width, height - label_height - 4), 1)
