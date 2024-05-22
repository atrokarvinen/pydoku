from models.square import Square
from techniques.models.connection import Connection


class CyclePart:
    def __init__(self, start: Square, end: Square, connection: Connection) -> None:
        self.start = start
        self.end = end
        self.connection = connection

    def __repr__(self) -> str:
        return f"CyclePart(({self.start.row}, {self.start.column}) => ({self.end.row}, {self.end.column}), {self.connection})"
