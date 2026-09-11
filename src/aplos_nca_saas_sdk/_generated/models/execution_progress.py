from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExecutionProgress")


@_attrs_define
class ExecutionProgress:
    """
    Attributes:
        completed_phases (int | Unset):
        total_phases (int | Unset):
        percent (float | Unset):
    """

    completed_phases: int | Unset = UNSET
    total_phases: int | Unset = UNSET
    percent: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed_phases = self.completed_phases

        total_phases = self.total_phases

        percent = self.percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if completed_phases is not UNSET:
            field_dict["completedPhases"] = completed_phases
        if total_phases is not UNSET:
            field_dict["totalPhases"] = total_phases
        if percent is not UNSET:
            field_dict["percent"] = percent

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        completed_phases = d.pop("completedPhases", UNSET)

        total_phases = d.pop("totalPhases", UNSET)

        percent = d.pop("percent", UNSET)

        execution_progress = cls(
            completed_phases=completed_phases,
            total_phases=total_phases,
            percent=percent,
        )

        execution_progress.additional_properties = d
        return execution_progress

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
