from sys import platform
from brush import Brush
import asyncio
import pygame

async def main() -> None:
    """ entrypoint for pygbag with main loop """
    pygame.display.init()
    pygame.display.set_caption("whiteboard")

    if platform == "emscripten":
        from platform import window
        display = pygame.display.set_mode((window.innerWidth, window.innerHeight))
        brush = Brush(display); FPS: int = 60
        brush.init_not_scroll_delay(FPS / 6)
    else:
        pygame.display.set_icon(pygame.image.load("favicon.png"))
        display = pygame.display.set_mode((1066, 600))
        brush = Brush(display); FPS: int = 120
        brush.init_not_scroll_delay(FPS / 10)
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
            if (event.type == pygame.MULTIGESTURE) and (event.pinched != 0.0):
                brush.is_size_incr = 2 * (event.pinched > 0) - 1
            if event.type == pygame.FINGERUP:
                num_fingers = max(num_fingers-1, 0)
                brush.is_size_incr = 0

            if event.type == pygame.MOUSEWHEEL:
                brush.is_size_incr = event.y
                brush.reset_not_scroll_delay()

            if (
                event.type == pygame.MOUSEBUTTONDOWN 
                and event.button not in {4, 5}
                and num_fingers < 2
            ):
                brush.is_drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                brush.is_drawing = False
                brush.is_size_incr = 0

            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_c):
                display.fill("black")
                brush.set_reset_preview()

        brush.decr_not_scroll_delay(FPS // 30)
        if brush.is_not_scroll_delay_over():
            brush.is_size_incr = 0
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
