from enum import StrEnum


class GetPingResponse200(StrEnum):
    PONG = "pong"

    def __str__(self) -> str:
        return str(self.value)
