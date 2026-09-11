from enum import Enum


class UserUpsertRequestStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    INVITED = "invited"

    def __str__(self) -> str:
        return str(self.value)
