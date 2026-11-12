class Zoom:
    def __init__(self, scroll_delay_frames: float = 0, not_scroll_delay_frames: float = 0):
        self.max_scroll_delay, self.max_not_scroll_delay = scroll_delay_frames, not_scroll_delay_frames
        self.scroll_delay, self.not_scroll_delay = 0, 0
        self.init_delay_decr(1)

    def init_delay_decr(self, by_frames: float) -> None:
        self.delay_decr = by_frames
    def decr_not_scroll_delay(self) -> None:
        self.not_scroll_delay = max(self.not_scroll_delay - self.delay_decr, 0)
    def decr_scroll_delay(self) -> None:
        self.scroll_delay = max(self.scroll_delay - self.delay_decr, 0)
    def decr(self) -> None:
        if self.scroll_delay: self.decr_scroll_delay()
        if self.not_scroll_delay: self.decr_not_scroll_delay()

    def reset_scroll_delay(self) -> None:
        self.scroll_delay = self.max_scroll_delay
    def reset_not_scroll_delay(self) -> None:
        self.not_scroll_delay = self.max_not_scroll_delay
    def reset(self) -> None:
        self.reset_scroll_delay(); self.reset_not_scroll_delay()

    def is_scroll_delay_over(self) -> bool:
        return self.scroll_delay == 0
    def is_not_scroll_delay_over(self) -> bool:
        return self.not_scroll_delay == 0
