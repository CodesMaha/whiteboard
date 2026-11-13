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

# TODO: 
# more keypress actions with more features
# equivalent ui menu for said actions
# make ui menu compulsory for mobile
# make ui menu able to be hidden otherwise
