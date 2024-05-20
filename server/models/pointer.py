from models.point import Point


class Pointer:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
        self.dashed = False

    def serialize(self):
        return {
            "start": self.start.serialize(),
            "end": self.end.serialize(),
            "dashed": self.dashed
        }
