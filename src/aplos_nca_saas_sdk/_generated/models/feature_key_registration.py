from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeatureKeyRegistration")


@_attrs_define
class FeatureKeyRegistration:
    """A registered feature key that rules can target.

    Attributes:
        feature_key (str):
        id (str | Unset):
        description (None | str | Unset):
        registered_by (None | str | Unset):
        registered_at (float | None | Unset):
        created_utc_ts (float | None | Unset):
        updated_utc_ts (float | None | Unset):
    """

    feature_key: str
    id: str | Unset = UNSET
    description: None | str | Unset = UNSET
    registered_by: None | str | Unset = UNSET
    registered_at: float | None | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feature_key = self.feature_key

        id = self.id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        registered_by: None | str | Unset
        if isinstance(self.registered_by, Unset):
            registered_by = UNSET
        else:
            registered_by = self.registered_by

        registered_at: float | None | Unset
        if isinstance(self.registered_at, Unset):
            registered_at = UNSET
        else:
            registered_at = self.registered_at

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
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if registered_by is not UNSET:
            field_dict["registeredBy"] = registered_by
        if registered_at is not UNSET:
            field_dict["registeredAt"] = registered_at
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        feature_key = d.pop("featureKey")

        id = d.pop("id", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_registered_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        registered_by = _parse_registered_by(d.pop("registeredBy", UNSET))

        def _parse_registered_at(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        registered_at = _parse_registered_at(d.pop("registeredAt", UNSET))

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

        feature_key_registration = cls(
            feature_key=feature_key,
            id=id,
            description=description,
            registered_by=registered_by,
            registered_at=registered_at,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        feature_key_registration.additional_properties = d
        return feature_key_registration

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
