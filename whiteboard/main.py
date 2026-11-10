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
    else:
        pygame.display.set_icon(pygame.image.load("favicon.png"))
        display = pygame.display.set_mode((1066, 600))
    display.fill("black")

    brush = Brush(display)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                brush.is_drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                brush.is_drawing = False
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_c):
                display.fill("black")

        brush.draw()
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
