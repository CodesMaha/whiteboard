""" configure actions for keypresses """

from typing import TYPE_CHECKING
if TYPE_CHECKING: from logic.event_handler import EventHandler

import pygame

class KeypressHandler:
    """ handle actions for keydown events """
    def __init__(self, event_handler: 'EventHandler'):
        self.events = event_handler

    def keydown(self, event: pygame.Event) -> None:
        if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE): # clear
            self.events.display.fill("black")
            self.events.brush.set_reset_preview()

    def emscripten_keydown(self, event: pygame.Event) -> None:
        """ called with regular/native keydown in WebEventHandler """
        if event.key == pygame.K_F5: # refresh
            self.events.window.location.reload()

class GestureHandler:
    """ handle some equivalents to KeypressHandler but
    for mobile/touchscreen. exceptions can be handled graphically
    """
    def __init__(self, mobile_event_handler: 'EventHandler'):
        self.events = mobile_event_handler
        self.fingers: dict[int, tuple[int, int]] = self.events.fingers

    def multigesture_2(self, event: pygame.Event) -> None:
        self.events.brush.is_size_incr = 2 * (event.pinched > 0) - 1
        self.events.not_zoom_delay.reset()

    def fingermotion_3(self, _: pygame.Event) -> None:
        dy_positive = []
        for dyx in self.fingers.values():
            if dyx is None: return
            dy_positive.append(dyx[1] > 0)
        if all(dy_positive): 
            self.events.display.fill("black")
            self.events.brush.set_reset_preview()

# TODO: 
# more keypress actions with more features
# equivalent ui menu for said actions
# make ui menu compulsory for mobile
# make ui menu able to be hidden otherwise
