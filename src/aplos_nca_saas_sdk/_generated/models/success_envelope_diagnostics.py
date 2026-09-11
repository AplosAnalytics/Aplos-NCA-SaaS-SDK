from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SuccessEnvelopeDiagnostics")


@_attrs_define
class SuccessEnvelopeDiagnostics:
    """
    Attributes:
        start_time_utc_ts (float | Unset):
        end_time_utc_ts (float | Unset):
        duration_ms (float | Unset):
    """

    start_time_utc_ts: float | Unset = UNSET
    end_time_utc_ts: float | Unset = UNSET
    duration_ms: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time_utc_ts = self.start_time_utc_ts

        end_time_utc_ts = self.end_time_utc_ts

        duration_ms = self.duration_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_time_utc_ts is not UNSET:
            field_dict["startTimeUtcTs"] = start_time_utc_ts
        if end_time_utc_ts is not UNSET:
            field_dict["endTimeUtcTs"] = end_time_utc_ts
        if duration_ms is not UNSET:
            field_dict["durationMs"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        start_time_utc_ts = d.pop("startTimeUtcTs", UNSET)

        end_time_utc_ts = d.pop("endTimeUtcTs", UNSET)

        duration_ms = d.pop("durationMs", UNSET)

        success_envelope_diagnostics = cls(
            start_time_utc_ts=start_time_utc_ts,
            end_time_utc_ts=end_time_utc_ts,
            duration_ms=duration_ms,
        )

        success_envelope_diagnostics.additional_properties = d
        return success_envelope_diagnostics

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
