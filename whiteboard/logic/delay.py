""" extra delay functionality beyond Clock.tick """

class Delay:
    """ currently delay before or after mouse scroll (pygame.MOUSEWHEEL) is detected 
    (or pygame.MULTIGESTURE pinched for mobile). this is currently used for
    brush size changes 
    """
    def __init__(self, delay_frames: float = 0, delay_decr: float = 1.0):
        self.max_delay = delay_frames
        self.delay: float = 0.0
        self.init_delay_decr(delay_decr)

    def init_delay_decr(self, by_frames: float) -> None:
        self.delay_decr = by_frames

    def decr(self) -> None:
        self.delay = max(self.delay - self.delay_decr, 0.0)
        
    def reset(self) -> None:
        self.delay = self.max_delay

    def is_over(self) -> bool:
        return self.delay == 0.0
