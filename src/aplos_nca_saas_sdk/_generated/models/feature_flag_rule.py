from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeatureFlagRule")


@_attrs_define
class FeatureFlagRule:
    """A feature-flag rule enabling/disabling a feature key for a given scope.

    Attributes:
        feature_key (str): The registered feature key this rule targets.
        scope (str): The scope level the rule applies to (e.g. global, tenant, user).
        enabled (bool):
        id (str | Unset):
        scope_id (None | str | Unset): Identifier within the scope (e.g. a tenant id or user id); null for global scope.
        created_utc_ts (float | None | Unset):
        updated_utc_ts (float | None | Unset):
    """

    feature_key: str
    scope: str
    enabled: bool
    id: str | Unset = UNSET
    scope_id: None | str | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feature_key = self.feature_key

        scope = self.scope

        enabled = self.enabled

        id = self.id

        scope_id: None | str | Unset
        if isinstance(self.scope_id, Unset):
            scope_id = UNSET
        else:
            scope_id = self.scope_id

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
                "featureKey": feature_key,
                "scope": scope,
                "enabled": enabled,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if scope_id is not UNSET:
            field_dict["scopeId"] = scope_id
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        feature_key = d.pop("featureKey")

        scope = d.pop("scope")

        enabled = d.pop("enabled")

        id = d.pop("id", UNSET)

        def _parse_scope_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scope_id = _parse_scope_id(d.pop("scopeId", UNSET))

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

        feature_flag_rule = cls(
            feature_key=feature_key,
            scope=scope,
            enabled=enabled,
            id=id,
            scope_id=scope_id,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        feature_flag_rule.additional_properties = d
        return feature_flag_rule

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
