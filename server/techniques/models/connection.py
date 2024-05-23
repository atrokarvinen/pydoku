from techniques.models.connectionType import ConnectionType
from techniques.models.regionType import RegionType


class Connection:
    def __init__(self, type: ConnectionType, region: RegionType, value: int) -> None:
        self.type = type
        self.region = region
        self.value = value

    def __eq__(self, other):
        return self.type == other.type \
            and self.region == other.region \
            and self.value == other.value

    def none():
        return Connection(ConnectionType.NONE, RegionType.NONE, 0)

    def __repr__(self) -> str:
        return f"({self.type}, {self.region})"

    def __hash__(self) -> int:
        return hash((self.type, self.region, self.value))
