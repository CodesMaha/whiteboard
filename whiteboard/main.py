from sys import platform as sys_platform
from graphics import Brush
from logic import *
import asyncio
import pygame

class App:
    def __init__(self) -> None:
        pygame.display.init()
        pygame.display.set_caption("whiteboard")

        if sys_platform == "emscripten":
            self.emscripten_setup()
        else:
            self.native_setup()

        self.clock = pygame.time.Clock()
        App.FPS = self.events.FPS

    def emscripten_setup(self) -> None:
        from platform import window
        display = pygame.display.set_mode((window.innerWidth, window.innerHeight))
        brush = Brush(display) 
        if window.screen.width < window.screen.height: # mobile
            self.events = TouchscreenEventHandler(display, brush, window)
        else: self.events = WebEventHandler(display, brush, window)

    def native_setup(self) -> None:
        pygame.display.set_icon(pygame.image.load("favicon.png"))
        display = pygame.display.set_mode((1066, 600))
        brush = Brush(display); self.events = EventHandler(display, brush)

    def step(self):
        self.clock.tick(App.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # mobile/touchscreen support (not properly tested)
            if event.type == pygame.FINGERDOWN:
                self.events.fingerdown(event)
            if event.type == pygame.MULTIGESTURE:
                self.events.multigesture(event)
            if event.type == pygame.FINGERUP:
                self.events.fingerup(event)

            if event.type == pygame.MOUSEWHEEL:
                self.events.mousewheel(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.events.mousebuttondown(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.events.mousebuttonup(event)

            if event.type == pygame.KEYDOWN:
                self.events.keydown(event)

        self.events.update()
        pygame.display.flip()
        return True

async def main() -> None:
    """ entrypoint for pygbag with main loop """
    try:
        app = App()
        while app.step():
            await asyncio.sleep(0)

    except Exception:
        if sys_platform == "emscripten":
            from platform import window
            from traceback import format_exc
            window.alert(format_exc()[-100:]) # otherwise hidden
        else: raise # leave it

    finally:
        pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
