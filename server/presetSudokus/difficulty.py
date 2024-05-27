from enum import Enum


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4
    EXTREME = 5

    def __str__(self):
        return self.name.lower().capitalize()

    def __repr__(self) -> str:
        return str(self)

    def serialize(self):
        return self.name
