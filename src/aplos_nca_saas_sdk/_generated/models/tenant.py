from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.tenant_plan_tier import TenantPlanTier
from ..models.tenant_status import TenantStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tenant_features import TenantFeatures


T = TypeVar("T", bound="Tenant")


@_attrs_define
class Tenant:
    """A customer organization (tenant) in the multi-tenant platform.

    Attributes:
        id (str):
        name (None | str | Unset):
        status (TenantStatus | Unset):  Example: active.
        plan_tier (TenantPlanTier | Unset):  Example: free.
        primary_contact_user_id (None | str | Unset):
        max_users (int | None | Unset): Maximum users allowed; null means unlimited.
        features (TenantFeatures | Unset): Per-tenant feature flags.
        allow_tenant_wide_access (bool | Unset):
        description (None | str | Unset):
        website (None | str | Unset):
        logo_url (None | str | Unset):
        created_utc_ts (float | None | Unset):
        updated_utc_ts (float | None | Unset):
    """

    id: str
    name: None | str | Unset = UNSET
    status: TenantStatus | Unset = UNSET
    plan_tier: TenantPlanTier | Unset = UNSET
    primary_contact_user_id: None | str | Unset = UNSET
    max_users: int | None | Unset = UNSET
    features: TenantFeatures | Unset = UNSET
    allow_tenant_wide_access: bool | Unset = UNSET
    description: None | str | Unset = UNSET
    website: None | str | Unset = UNSET
    logo_url: None | str | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        plan_tier: str | Unset = UNSET
        if not isinstance(self.plan_tier, Unset):
            plan_tier = self.plan_tier.value

        primary_contact_user_id: None | str | Unset
        if isinstance(self.primary_contact_user_id, Unset):
            primary_contact_user_id = UNSET
        else:
            primary_contact_user_id = self.primary_contact_user_id

        max_users: int | None | Unset
        if isinstance(self.max_users, Unset):
            max_users = UNSET
        else:
            max_users = self.max_users

        features: dict[str, Any] | Unset = UNSET
        if not isinstance(self.features, Unset):
            features = self.features.to_dict()

        allow_tenant_wide_access = self.allow_tenant_wide_access

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        website: None | str | Unset
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        created_utc_ts: float | None | Unset
        if isinstance(self.created_utc_ts, Unset):
            created_utc_ts = UNSET
        else:
            created_utc_ts = self.created_utc_ts

        updated_utc_ts: float | None | Unset
        if isinstance(self.updated_utc_ts, Unset):
            updated_utc_ts = UNSET
        else:
            updated_utc_ts = self.updated_utc_ts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status
        if plan_tier is not UNSET:
            field_dict["planTier"] = plan_tier
        if primary_contact_user_id is not UNSET:
            field_dict["primaryContactUserId"] = primary_contact_user_id
        if max_users is not UNSET:
            field_dict["maxUsers"] = max_users
        if features is not UNSET:
            field_dict["features"] = features
        if allow_tenant_wide_access is not UNSET:
            field_dict["allowTenantWideAccess"] = allow_tenant_wide_access
        if description is not UNSET:
            field_dict["description"] = description
        if website is not UNSET:
            field_dict["website"] = website
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.tenant_features import TenantFeatures

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        _status = d.pop("status", UNSET)
        status: TenantStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TenantStatus(_status)

        _plan_tier = d.pop("planTier", UNSET)
        plan_tier: TenantPlanTier | Unset
        if isinstance(_plan_tier, Unset):
            plan_tier = UNSET
        else:
            plan_tier = TenantPlanTier(_plan_tier)

        def _parse_primary_contact_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        primary_contact_user_id = _parse_primary_contact_user_id(
            d.pop("primaryContactUserId", UNSET)
        )

        def _parse_max_users(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_users = _parse_max_users(d.pop("maxUsers", UNSET))

        _features = d.pop("features", UNSET)
        features: TenantFeatures | Unset
        if isinstance(_features, Unset):
            features = UNSET
        else:
            features = TenantFeatures.from_dict(_features)

        allow_tenant_wide_access = d.pop("allowTenantWideAccess", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_website(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        website = _parse_website(d.pop("website", UNSET))

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logoUrl", UNSET))

        def _parse_created_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        created_utc_ts = _parse_created_utc_ts(d.pop("createdUtcTs", UNSET))

        def _parse_updated_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        updated_utc_ts = _parse_updated_utc_ts(d.pop("updatedUtcTs", UNSET))

        tenant = cls(
            id=id,
            name=name,
            status=status,
            plan_tier=plan_tier,
            primary_contact_user_id=primary_contact_user_id,
            max_users=max_users,
            features=features,
            allow_tenant_wide_access=allow_tenant_wide_access,
            description=description,
            website=website,
            logo_url=logo_url,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        tenant.additional_properties = d
        return tenant

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
