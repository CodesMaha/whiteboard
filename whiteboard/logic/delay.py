class NotScrollDelay:
    def __init__(self, not_scroll_delay_frames: float = 0):
        self.max_not_scroll_delay = not_scroll_delay_frames
        self.not_scroll_delay: float = 0.0
        self.init_delay_decr(1.0)

    def init_delay_decr(self, by_frames: float) -> None:
        self.delay_decr = by_frames

    def decr(self) -> None:
        self.not_scroll_delay = max(self.not_scroll_delay - self.delay_decr, 0.0)
        
    def reset(self) -> None:
        self.not_scroll_delay = self.max_not_scroll_delay

    def is_over(self) -> bool:
        return self.not_scroll_delay == 0.0
