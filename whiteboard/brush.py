import pygame
from typing import Generator

type P = pygame.math.Vector2

class Brush:
    SIZE_INCR: int = 5
    """ adjustable properties and functions of drawing brush """
    def __init__(self, display: pygame.Surface):
        self.display = display
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
        return self._size 
    @size.setter
    def size(self, new: int) -> None:
        self._size = max(new, 2)
        self.update_texture()

    def incr_size(self, coefficient: int, incr: int = 0) -> None:
        incr = incr or Brush.SIZE_INCR
        self.size += coefficient * incr
    def incr_size_mobile(self, incr: int = 0) -> None:
        if not self.is_size_incr:
            return
        self.incr_size(self.is_size_incr, incr)

    @staticmethod
    def de_casteljau(p0: P, p1: P, *, precision: int = 2) -> Generator[P, None, None]:
        for t in range(10**precision + 1):
            t *= 10**(-precision)
            yield (1 - t) * p0 + (t * p1)

    def draw(self) -> None:
        """ draw texture at mouse pos if is_drawing """
        if (not self.is_drawing) or (self.is_size_incr):
            return
        curr_pos = pygame.Vector2(pygame.mouse.get_pos())
        for p in Brush.de_casteljau(self.prev_pos, curr_pos):
            self.display.blit(self.texture, self.texture.get_rect(center=p))
        self.prev_pos = curr_pos; curr_pos = None

    def update_texture(self) -> None:
        di = lambda x: (x, x)
        self.texture = pygame.surface.Surface(di(self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            self.texture, "white", di(self.size // 2), self.size // 2
        )
