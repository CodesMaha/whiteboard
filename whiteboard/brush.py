import pygame
from math import ceil, exp
from typing import Generator

type P = pygame.math.Vector2

class Brush:
    SIZE_INCR: int = 2
    """ adjustable properties and functions of drawing brush """
    def __init__(self, display: pygame.Surface):
        self.display = display
        self.set_reset_preview()
        self.is_drawing = False
        self.size = display.height // 100
        self.is_size_incr = 0

    @property
    def is_drawing(self) -> bool:
        return self._is_drawing
    @is_drawing.setter
    def is_drawing(self, new: bool) -> None:
        self._is_drawing = new
        if self.is_drawing:
            self.prev_pos: P | None = pygame.Vector2(pygame.mouse.get_pos())
        else:
            self.prev_pos: None | P = None

    @property
    def is_size_incr(self) -> int:
        """0 False; 1 True; -1 decr"""
        return self._is_size_incr
    @is_size_incr.setter
    def is_size_incr(self, new: int) -> None:
        self._is_size_incr = new

    @property
    def size(self) -> int:
        """ circular brush size, where the minimum is 2 (r=1) """
        return self._size 
    @size.setter
    def size(self, new: int) -> None:
        self._size = min(max(new, 2), self.display.height)
        self.update_texture()

    def incr_size(self, incr: int = 0) -> None:
        """ incr brush size by Brush.SIZE_INCR according
        to self.is_size_incr
        """
        if not self.is_size_incr:
            return

        incr = incr or Brush.SIZE_INCR
        self.size += self.is_size_incr * ceil(min(incr * (self.size / 20) ** 1.8, 30))

    @staticmethod
    def de_casteljau(p0: P, p1: P, *, precision: int = 2) -> Generator[P, None, None]:
        """ points lying on a straight line segment """
        for t in range(10**precision + 1):
            t *= 10**(-precision)
            yield (1 - t) * p0 + (t * p1)

    def draw_texture(self) -> None:
        """ draw texture at mouse pos if is_drawing """
        if (not self.is_drawing) or (self.is_size_incr):
            return
        self.reset_preview()
        curr_pos = pygame.Vector2(pygame.mouse.get_pos())
        for p in Brush.de_casteljau(self.prev_pos, curr_pos):
            self.display.blit(self.texture, self.texture.get_rect(center=p))
        self.prev_pos = curr_pos; curr_pos = None
        self._pre_preview = self.display.copy()

    def update_texture(self) -> None:
        """ what actually gets drawn onto the display to mimic a brush stroke """
        di = lambda x: (x, x)
        self.texture = pygame.surface.Surface(di(self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            self.texture, "white", di(self.size // 2), self.size / 2
        )

    def draw_preview(self) -> None:
        """ let user preview self.size if self.is_size_incr """
        self.reset_preview()
        pygame.draw.circle(
            self.display, "white", pygame.mouse.get_pos(), 
            self.size / 2, 2
        )
    def set_reset_preview(self) -> None:
        """ copy display before drawing to avoid 
        brush preview being drawn onto screen """
        self._pre_preview = self.display.copy()
    def reset_preview(self) -> None:
        """ draw over brush preview with saved copy of display """
        self.display.blit(self._pre_preview)

    def init_not_scroll_delay(self, delay_frames: float) -> None:
        """ define the height of the delay after pygame.MOUSEWHEEL ev """
        self.max_not_scroll_delay = self.not_scroll_delay = delay_frames
    def reset_not_scroll_delay(self):
        self.not_scroll_delay = self.max_not_scroll_delay
    def decr_not_scroll_delay(self, by_frames: float = 0.5) -> None:
        self.not_scroll_delay = max(self.not_scroll_delay - by_frames, 0)
    def is_not_scroll_delay_over(self) -> bool:
        return self.not_scroll_delay == 0
