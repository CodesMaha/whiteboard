import pygame

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

    def get_num_fingers(self) -> int:
        return 1 # mouse

class MobileZoom(Zoom):
    def __init__(self, scroll_delay_frames: float = 0, not_scroll_delay_frames: float = 0):
        super().__init__(scroll_delay_frames, not_scroll_delay_frames)
        self.prev_fingers: dict[int, tuple[float, float]] = {}
        self.fingers: dict[int, tuple[float, float]] = {}

    def fingermotion(self, event: pygame.event.Event) -> None:
        if event.finger_id in self.fingers:
            self.prev_fingers[event.finger_id] = self.fingers[event.finger_id]
        self.fingers[event.finger_id] = event.x, event.y
    def fingerup(self, event: pygame.event.Event) -> None:
        self.fingers.pop(event.finger_id, None)
    def get_num_fingers(self) -> int:
        return len(self.fingers)

    def get_d_dist(self) -> float:
        if (self.get_num_fingers() < 2) or (len(self.prev_fingers) < 2):
            return 0.0
        fingers = list(self.fingers.values())[:2]
        prev_fingers = list(self.prev_fingers.values())[:2]
        df = abs(fingers[0][0] - fingers[1][0]) + abs(fingers[0][1] - fingers[1][1])
        di = abs(prev_fingers[0][0] - prev_fingers[1][0]) + abs(prev_fingers[0][1] - prev_fingers[1][1])
        return df - di
