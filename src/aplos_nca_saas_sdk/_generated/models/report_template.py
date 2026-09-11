from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportTemplate")


@_attrs_define
class ReportTemplate:
    """A custom report template owned by a tenant.

    Attributes:
        id (str):
        tenant_id (str | Unset):
        name (None | str | Unset):
        ownership_level (None | str | Unset): Ownership scope of the template (e.g. tenant, platform).
        status (str | Unset):
        version_count (int | Unset):
        latest_version (int | Unset):
        created_utc_ts (float | None | Unset):
        updated_utc_ts (float | None | Unset):
    """

    id: str
    tenant_id: str | Unset = UNSET
    name: None | str | Unset = UNSET
    ownership_level: None | str | Unset = UNSET
    status: str | Unset = UNSET
    version_count: int | Unset = UNSET
    latest_version: int | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        ownership_level: None | str | Unset
        if isinstance(self.ownership_level, Unset):
            ownership_level = UNSET
        else:
            ownership_level = self.ownership_level

        status = self.status

        version_count = self.version_count

        latest_version = self.latest_version

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
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if name is not UNSET:
            field_dict["name"] = name
        if ownership_level is not UNSET:
            field_dict["ownershipLevel"] = ownership_level
        if status is not UNSET:
            field_dict["status"] = status
        if version_count is not UNSET:
            field_dict["versionCount"] = version_count
        if latest_version is not UNSET:
            field_dict["latestVersion"] = latest_version
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        tenant_id = d.pop("tenantId", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_ownership_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ownership_level = _parse_ownership_level(d.pop("ownershipLevel", UNSET))

        status = d.pop("status", UNSET)

        version_count = d.pop("versionCount", UNSET)

        latest_version = d.pop("latestVersion", UNSET)

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

        report_template = cls(
            id=id,
            tenant_id=tenant_id,
            name=name,
            ownership_level=ownership_level,
            status=status,
            version_count=version_count,
            latest_version=latest_version,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        report_template.additional_properties = d
        return report_template

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
