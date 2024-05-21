from models.point import Point


class Pointer:
    def __init__(self, start: Point, end: Point, dashed=False, bidirectional=False) -> None:
        self.start = start
        self.end = end
        self.dashed = dashed
        self.bidirectional = bidirectional

    def serialize(self):
        return {
            "start": self.start.serialize(),
            "end": self.end.serialize(),
            "dashed": self.dashed,
            "bidirectional": self.bidirectional
        }
