from sys import platform
from brush import Brush
from ui import ZoomDelay
import asyncio
import pygame

async def main() -> None:
    """ entrypoint for pygbag with main loop """
    pygame.display.init()
    pygame.display.set_caption("whiteboard")

    if platform == "emscripten":
        from platform import window
        is_mobile = window.screen.width < window.screen.height
        display = pygame.display.set_mode((window.innerWidth, window.innerHeight))
        brush = Brush(display); FPS: int = 60
        zoom = ZoomDelay(0, FPS / 6)
    else:
        is_mobile = False # not tested at all
        pygame.display.set_icon(pygame.image.load("favicon.png"))
        display = pygame.display.set_mode((1066, 600))
        brush = Brush(display); FPS: int = 120
        zoom = ZoomDelay(0, FPS / 10)
    if is_mobile:
        zoom = ZoomDelay(FPS / 24, 0)
    zoom.init_delay_decr(FPS / 30)
    clock = pygame.time.Clock()
    num_fingers: int = 0
    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # mobile support (not properly tested)
            if event.type == pygame.FINGERDOWN:
                num_fingers += 1
            if (
                event.type == pygame.MULTIGESTURE
                and zoom.is_scroll_delay_over()  
                and event.pinched != 0.0
            ):
                brush.is_size_incr = 2 * (event.pinched > 0) - 1
                zoom.reset()
            if event.type == pygame.FINGERUP:
                num_fingers = max(num_fingers-1, 0)

            if event.type == pygame.MOUSEWHEEL and zoom.is_scroll_delay_over():
                brush.is_size_incr = event.y
                zoom.reset()

            if (
                event.type == pygame.MOUSEBUTTONDOWN 
                and event.button not in {4, 5}
                and num_fingers < 2
            ):
                brush.is_drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                brush.is_drawing = False

            if event.type == pygame.KEYDOWN:
                # clear
                if event.key == pygame.K_c:
                    display.fill("black")
                    brush.set_reset_preview()
                # refresh
                if (platform == "emscripten") and (event.key == pygame.K_F5):
                    window.location.reload()

        zoom.decr()
        if zoom.is_not_scroll_delay_over():
            brush.is_size_incr = 0
        if zoom.is_scroll_delay_over():
            brush.incr_size()
        brush.draw_texture()
        if not pygame.event.peek(pygame.FINGERUP):
            brush.draw_preview()
        else:
            brush.reset_preview()
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
