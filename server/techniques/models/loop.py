from models.square import Square
from techniques.models.loopPart import LoopPart


class Loop:
    def __init__(self):
        self.parts: list[LoopPart] = []

    def append(self, part: LoopPart):
        self.parts.append(part)

    def get_latest_part(self) -> LoopPart:
        return self.parts[-1]

    def is_nice(self, loop) -> bool:
        return False

    def is_distinct_strong(self, loop) -> bool:
        return False

    def is_distinct_weak(self, loop) -> bool:
        return False
