class Solver:
    def __init__(self, name: str) -> None:
        self.id: str = None
        self.name = name
        self.priority: int = -1
        self.enabled: bool = True

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "enabled": self.enabled,
        }
