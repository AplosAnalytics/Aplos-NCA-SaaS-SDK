from enum import Enum


class QueueAcceptedResponseStatus(str, Enum):
    QUEUED = "queued"
    THROTTLED = "throttled"

    def __str__(self) -> str:
        return str(self.value)
