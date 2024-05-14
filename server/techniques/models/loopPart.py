from models.square import Square


class LoopPart:
    def __init__(self, start: Square, end: Square, type: str) -> None:
        self.start = start
        self.end = end
        self.type = type

    def is_weak(self) -> bool:
        return self.type == "weak"

    def is_strong(self) -> bool:
        return self.type == "strong"
