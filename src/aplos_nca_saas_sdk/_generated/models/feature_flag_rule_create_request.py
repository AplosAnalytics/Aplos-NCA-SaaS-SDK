from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeatureFlagRuleCreateRequest")


@_attrs_define
class FeatureFlagRuleCreateRequest:
    """Request body to create a feature-flag rule.

    Attributes:
        feature_key (str):
        scope (str):
        scope_id (None | str | Unset):
        enabled (bool | Unset):
    """

    feature_key: str
    scope: str
    scope_id: None | str | Unset = UNSET
    enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feature_key = self.feature_key

        scope = self.scope

        scope_id: None | str | Unset
        if isinstance(self.scope_id, Unset):
            scope_id = UNSET
        else:
            scope_id = self.scope_id

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "featureKey": feature_key,
                "scope": scope,
            }
        )
        if scope_id is not UNSET:
            field_dict["scopeId"] = scope_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        feature_key = d.pop("featureKey")

        scope = d.pop("scope")

        def _parse_scope_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scope_id = _parse_scope_id(d.pop("scopeId", UNSET))

        enabled = d.pop("enabled", UNSET)

        feature_flag_rule_create_request = cls(
            feature_key=feature_key,
            scope=scope,
            scope_id=scope_id,
            enabled=enabled,
        )

        feature_flag_rule_create_request.additional_properties = d
        return feature_flag_rule_create_request

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
