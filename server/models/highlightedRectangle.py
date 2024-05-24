from models.point import Point


class HighlightedRectangle():
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def serialize(self) -> dict:
        return {
            "start": self.start.serialize(),
            "end": self.end.serialize()
        }
