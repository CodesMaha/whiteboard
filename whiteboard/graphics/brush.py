""" texture blit onto display, dest pygame.mouse """

import pygame
from config import colour
from math import ceil
from typing import Generator

type P = pygame.math.Vector2

class Brush:
    """ adjustable properties and functions of drawing brush """
    SIZE_INCR: int = 2
    def __init__(self, display: pygame.Surface):
        self.display = display
        self.set_reset_preview()
        self.is_drawing = False
        self.colour = colour["white"]
        """ colour of brush texture """
        self.size = display.height // 100
        self.is_size_incr = 0
        """ 0 False; 1 True; -1 decr for self.size """

    @property
    def is_drawing(self) -> bool:
        """ whether or not to track pygame.mouse to draw """
        return self._is_drawing
    @is_drawing.setter
    def is_drawing(self, new: bool) -> None:
        self._is_drawing = new
        if self.is_drawing:
            self.prev_pos: P | None = pygame.Vector2(pygame.mouse.get_pos())
        else:
            self.prev_pos: None | P = None

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
        self.size += self.is_size_incr * ceil(min(incr * (self.size / 20) ** 1.8, 10))

    @staticmethod
    def dist(p0: P, p1: P) -> float: return (p0 - p1).length()
    def de_casteljau(self, p0: P, p1: P) -> Generator[P, None, None]:
        """ points lying on a straight line segment; no. points based on
        Brush.dist between pts and self.size 
        """
        total = (self.dist(p0, p1) or 1) / (self.size / 4); t = -1/total
        for _ in range(ceil(total)):
            t += 1/total # t b/w 0 && 1
            if t > 1: break
            yield (1 - t) * p0 + (t * p1)

    def draw_texture(self) -> None:
        """ draw texture at mouse pos if is_drawing """
        if (not self.is_drawing) or (self.is_size_incr):
            return
        self.reset_preview()
        curr_pos = pygame.Vector2(pygame.mouse.get_pos())
        for p in self.de_casteljau(self.prev_pos, curr_pos):
            self.display.blit(self.texture, self.texture.get_rect(center=p))
        self.prev_pos = curr_pos; curr_pos = None
        self._pre_preview = self.display.copy()

    def update_texture(self) -> None:
        """ what actually gets drawn onto the display to mimic a brush stroke """
        di = lambda x: (x, x)
        self.texture = pygame.surface.Surface(di(self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            self.texture, self.colour, di(self.size // 2), self.size / 2
        )

    def draw_preview(self) -> None:
        """ let user preview self.size if self.is_size_incr """
        self.reset_preview()
        pygame.draw.circle(
            self.display, colour["light_gray"], pygame.mouse.get_pos(), 
            self.size / 2, 2
        )
    def set_reset_preview(self) -> None:
        """ copy display before drawing to avoid 
        brush preview being drawn onto screen """
        self._pre_preview = self.display.copy()
    def reset_preview(self) -> None:
        """ draw over brush preview with saved copy of display """
        self.display.blit(self._pre_preview)
