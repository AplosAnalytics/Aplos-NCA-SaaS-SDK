from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.tenant_upsert_request_plan_tier import TenantUpsertRequestPlanTier
from ..models.tenant_upsert_request_status import TenantUpsertRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tenant_upsert_request_features import TenantUpsertRequestFeatures


T = TypeVar("T", bound="TenantUpsertRequest")


@_attrs_define
class TenantUpsertRequest:
    """Request body to create or update a tenant. On create, name is required; on update (with a tenant id in the path),
    only provided fields change.

        Attributes:
            name (str | Unset):
            status (TenantUpsertRequestStatus | Unset):
            plan_tier (TenantUpsertRequestPlanTier | Unset):
            primary_contact_user_id (str | Unset):
            max_users (int | None | Unset):
            features (TenantUpsertRequestFeatures | Unset):
            allow_tenant_wide_access (bool | Unset):
            description (str | Unset):
            website (str | Unset):
            logo_url (str | Unset):
    """

    name: str | Unset = UNSET
    status: TenantUpsertRequestStatus | Unset = UNSET
    plan_tier: TenantUpsertRequestPlanTier | Unset = UNSET
    primary_contact_user_id: str | Unset = UNSET
    max_users: int | None | Unset = UNSET
    features: TenantUpsertRequestFeatures | Unset = UNSET
    allow_tenant_wide_access: bool | Unset = UNSET
    description: str | Unset = UNSET
    website: str | Unset = UNSET
    logo_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        plan_tier: str | Unset = UNSET
        if not isinstance(self.plan_tier, Unset):
            plan_tier = self.plan_tier.value

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

        description = self.description

        website = self.website

        logo_url = self.logo_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.tenant_upsert_request_features import TenantUpsertRequestFeatures

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _status = d.pop("status", UNSET)
        status: TenantUpsertRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TenantUpsertRequestStatus(_status)

        _plan_tier = d.pop("planTier", UNSET)
        plan_tier: TenantUpsertRequestPlanTier | Unset
        if isinstance(_plan_tier, Unset):
            plan_tier = UNSET
        else:
            plan_tier = TenantUpsertRequestPlanTier(_plan_tier)

        primary_contact_user_id = d.pop("primaryContactUserId", UNSET)

        def _parse_max_users(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_users = _parse_max_users(d.pop("maxUsers", UNSET))

        _features = d.pop("features", UNSET)
        features: TenantUpsertRequestFeatures | Unset
        if isinstance(_features, Unset):
            features = UNSET
        else:
            features = TenantUpsertRequestFeatures.from_dict(_features)

        allow_tenant_wide_access = d.pop("allowTenantWideAccess", UNSET)

        description = d.pop("description", UNSET)

        website = d.pop("website", UNSET)

        logo_url = d.pop("logoUrl", UNSET)

        tenant_upsert_request = cls(
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
        )

        tenant_upsert_request.additional_properties = d
        return tenant_upsert_request

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
