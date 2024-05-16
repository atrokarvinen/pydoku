class HighlightedRegion:
    def __init__(self, type: str, value: int) -> None:
        self.type = type
        self.value = value

    def serialize(self) -> dict:
        return {
            "type": self.type,
            "value": self.value
        }
