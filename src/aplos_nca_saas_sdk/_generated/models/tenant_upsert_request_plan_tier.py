from enum import Enum


class TenantUpsertRequestPlanTier(str, Enum):
    BASIC = "basic"
    DEVELOPMENT = "development"
    ENTERPRISE = "enterprise"
    FREE = "free"
    PRO = "pro"

    def __str__(self) -> str:
        return str(self.value)
