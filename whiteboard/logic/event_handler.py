""" handling events (according to detected os) individually """

import pygame
from logic.key_gesture import KeypressHandler, GestureHandler
from graphics import Brush
from logic import Delay

class EventHandler:
    """ handle native events (acting as base class) """
    FPS = 120
    def __init__(self, display: pygame.Surface, brush: Brush):
        self.display, self.brush = display, brush
        self.keypresses = KeypressHandler(self)

    def update(self) -> None:
        """ custom calls (flip and sleep outside) """
        self.brush.incr_size()
        self.brush.draw_texture()
        self.brush.draw_preview()
        self.brush.is_size_incr = 0

    def mousewheel(self, event: pygame.Event) -> None:
        if event.touch: return
        self.brush.is_size_incr = event.y

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
        self.window = window

    def keydown(self, event):
        super().keydown(event)
        self.keypresses.emscripten_keydown(event)

class TouchscreenEventHandler(WebEventHandler):
    """ handle web and touchscreen events (from pygbag) """
    def __init__(self, display, brush, window):
        super().__init__(display, brush, window)
        # avoid interfering between features
        self.before_delay = Delay(self.FPS / 20, self.FPS / 60)
        self.after_delay = Delay(self.FPS / 20, self.FPS / 60)

        # dict[finger_id, tuple[dx, dy]] from fingermotion
        self.fingers: dict[int, tuple[int, int] | None] = {}
        self.gestures = GestureHandler(self)

    def update(self):
        self.before_delay.decr(); self.after_delay.decr()
        self.brush.incr_size()
        self.brush.draw_texture()
        if self.brush.is_size_incr: # when not drawing
            self.brush.draw_preview()

    def fingerdown(self, event: pygame.Event):
        self.fingers[event.finger_id] = None
        if self.before_delay.is_over(): # dot (single click)
            self.brush.is_drawing = len(self.fingers) == 1
            self.after_delay.reset()

    def fingermotion(self, event):
        if not self.after_delay.is_over(): return
        self.fingers[event.finger_id] = event.dx, event.dy
        if len(self.fingers) == 3:
            self.gestures.fingermotion_3(event)
            self.after_delay.reset()

    def multigesture(self, event):
        self.brush.is_drawing = False # no multi-finger drawing
        if event.pinched == 0.0: return
        if (
            event.num_fingers == 2 
            and self.after_delay.is_over()
            and self.before_delay.is_over()
        ): 
            self.gestures.multigesture_2(event)
            self.after_delay.reset()

    def fingerup(self, event):
        self.fingers.pop(event.finger_id, None)
        # at least one finger to draw
        if len(self.fingers) == 0:
            self.brush.is_drawing = False
            self.before_delay.reset()
