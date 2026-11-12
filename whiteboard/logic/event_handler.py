""" handling events (according to detected os) individually """

import pygame
from graphics import Brush
from logic import NotScrollDelay

class EventHandler:
    """ handle native events (acting as base class) """
    FPS = 120
    def __init__(self, display: pygame.Surface, brush: Brush):
        self.display, self.brush = display, brush
        self.not_zoom_delay = NotScrollDelay(self.FPS / 10)
        self.not_zoom_delay.init_delay_decr(self.FPS / 30)

    def update(self) -> None:
        """ custom calls (flip and sleep outside) """
        self.not_zoom_delay.decr()
        if self.not_zoom_delay.is_over():
            self.brush.is_size_incr = 0
        self.brush.incr_size()
        self.brush.draw_texture()
        self.brush.draw_preview()

    def mousewheel(self, event: pygame.Event) -> None:
        if event.touch: return
        self.brush.is_size_incr = event.y
        self.not_zoom_delay.reset()

    def mousebuttondown(self, event: pygame.Event) -> None:
        if (event.button in {4, 5}) or (event.touch): return
        self.brush.is_drawing = True

    def mousebuttonup(self, event: pygame.Event) -> None:
        if event.touch: return
        self.brush.is_drawing = False

    def keydown(self, event: pygame.Event) -> None:
        if event.key == pygame.K_c:
            self.display.fill("black")
            self.brush.set_reset_preview()

    def fingerdown(self, event: pygame.Event) -> None:
        pass

    def multigesture(self, event: pygame.Event) -> None:
        pass

    def fingerup(self, event: pygame.Event) -> None:
        pass

class WebEventHandler(EventHandler):
    """ handle web events (from pygbag) """
    FPS = 60 # browser limit
    def __init__(self, display: pygame.Surface, brush: Brush, window):
        super().__init__(display, brush)
        self.not_zoom_delay.max_not_scroll_delay = WebEventHandler.FPS / 6
        self.window = window

    def keydown(self, event):
        super().keydown(event)
        if event.key == pygame.K_F5:
            self.window.location.reload()

class TouchscreenEventHandler(WebEventHandler):
    """ handle web and touchscreen events (from pygbag) """
    def __init__(self, display, brush, window):
        super().__init__(display, brush, window)
        self.fingers: set[int] = set()

    def update(self):
        self.not_zoom_delay.decr()
        if self.not_zoom_delay.is_over():
            self.brush.is_size_incr = 0
        self.brush.incr_size()
        self.brush.draw_texture()
        if len(self.fingers) > 1: # when not drawing
            self.brush.draw_preview()

    def fingerdown(self, event):
        self.fingers.add(event.finger_id)
        if len(self.fingers) > 1: # no multi-finger drawing
            self.brush.is_drawing = False
        else: self.brush.is_drawing = True

    def multigesture(self, event):
        if event.pinched == 0.0: return
        self.brush.is_size_incr = 2 * (event.pinched > 0) - 1
        self.not_zoom_delay.reset()

    def fingerup(self, event):
        self.fingers.discard(event.finger_id)
        if len(self.fingers) == 0: 
            self.brush.is_drawing = 0
