from enum import Enum


class TenantPlanTier(str, Enum):
    BASIC = "basic"
    DEVELOPMENT = "development"
    ENTERPRISE = "enterprise"
    FREE = "free"
    PRO = "pro"

    def __str__(self) -> str:
        return str(self.value)
