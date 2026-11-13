""" handling events (according to detected os) individually """

import pygame
from logic.key_gesture import KeypressHandler, GestureHandler
from graphics import Brush
from logic import NotScrollDelay

class EventHandler:
    """ handle native events (acting as base class) """
    FPS = 120
    def __init__(self, display: pygame.Surface, brush: Brush):
        self.display, self.brush = display, brush
        self.not_zoom_delay = NotScrollDelay(self.FPS / 10)
        self.not_zoom_delay.init_delay_decr(self.FPS / 30)
        self.keypresses = KeypressHandler(self)

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
        self.keypresses.keydown(event)

    def fingerdown(self, event: pygame.Event) -> None:
        pass

    def fingermotion(self, event: pygame.Event) -> None:
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
        self.keypresses.emscripten_keydown(event)

class TouchscreenEventHandler(WebEventHandler):
    """ handle web and touchscreen events (from pygbag) """
    def __init__(self, display, brush, window):
        super().__init__(display, brush, window)
        self.gestures = GestureHandler(self)
        # dict[finger_id, tuple[dx, dy]] from fingermotion
        self.fingers: dict[int, tuple[int, int] | None] = {}

    def update(self):
        self.not_zoom_delay.decr()
        if self.not_zoom_delay.is_over():
            self.brush.is_size_incr = 0
        self.brush.incr_size()
        self.brush.draw_texture()
        if len(self.fingers) > 1: # when not drawing
            self.brush.draw_preview()

    def fingerdown(self, event: pygame.Event):
        self.fingers[event.finger_id] = None
        self.brush.is_drawing = len(self.fingers) == 1 # dot (single click)

    def fingermotion(self, event):
        self.fingers[event.finger_id] = event.dx, event.dy
        if len(self.fingers) == 3:
            self.gestures.fingermotion_3(event)

    def multigesture(self, event):
        self.brush.is_drawing = False # no multi-finger drawing
        if event.pinched == 0.0: return
        if event.num_fingers == 2: 
            self.gestures.multigesture_2(event)

    def fingerup(self, event):
        self.fingers.pop(event.finger_id, None)
        if len(self.fingers) == 0: 
            self.brush.is_drawing = 0
