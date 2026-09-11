from enum import Enum


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    DISABLED = "disabled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"
    PENDING = "pending"
    READY = "ready"
    RESTRICTED = "restricted"
    SUPERSEDED = "superseded"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)
