from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_step_stats_type_0 import ExecutionStepStatsType0


T = TypeVar("T", bound="ExecutionStep")


@_attrs_define
class ExecutionStep:
    """A single step within an execution phase.

    Attributes:
        order (int | None | Unset):
        step_type (None | str | Unset):
        status (None | str | Unset):
        version (None | str | Unset):
        started_utc (None | str | Unset):
        completed_utc (None | str | Unset):
        duration_ms (int | None | Unset):
        duration_human (None | str | Unset):
        stats (ExecutionStepStatsType0 | None | Unset):
    """

    order: int | None | Unset = UNSET
    step_type: None | str | Unset = UNSET
    status: None | str | Unset = UNSET
    version: None | str | Unset = UNSET
    started_utc: None | str | Unset = UNSET
    completed_utc: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    duration_human: None | str | Unset = UNSET
    stats: ExecutionStepStatsType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.execution_step_stats_type_0 import ExecutionStepStatsType0

        order: int | None | Unset
        if isinstance(self.order, Unset):
            order = UNSET
        else:
            order = self.order

        step_type: None | str | Unset
        if isinstance(self.step_type, Unset):
            step_type = UNSET
        else:
            step_type = self.step_type

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        version: None | str | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        started_utc: None | str | Unset
        if isinstance(self.started_utc, Unset):
            started_utc = UNSET
        else:
            started_utc = self.started_utc

        completed_utc: None | str | Unset
        if isinstance(self.completed_utc, Unset):
            completed_utc = UNSET
        else:
            completed_utc = self.completed_utc

        duration_ms: int | None | Unset
        if isinstance(self.duration_ms, Unset):
            duration_ms = UNSET
        else:
            duration_ms = self.duration_ms

        duration_human: None | str | Unset
        if isinstance(self.duration_human, Unset):
            duration_human = UNSET
        else:
            duration_human = self.duration_human

        stats: dict[str, Any] | None | Unset
        if isinstance(self.stats, Unset):
            stats = UNSET
        elif isinstance(self.stats, ExecutionStepStatsType0):
            stats = self.stats.to_dict()
        else:
            stats = self.stats

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if step_type is not UNSET:
            field_dict["stepType"] = step_type
        if status is not UNSET:
            field_dict["status"] = status
        if version is not UNSET:
            field_dict["version"] = version
        if started_utc is not UNSET:
            field_dict["startedUtc"] = started_utc
        if completed_utc is not UNSET:
            field_dict["completedUtc"] = completed_utc
        if duration_ms is not UNSET:
            field_dict["durationMs"] = duration_ms
        if duration_human is not UNSET:
            field_dict["durationHuman"] = duration_human
        if stats is not UNSET:
            field_dict["stats"] = stats

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.execution_step_stats_type_0 import ExecutionStepStatsType0

        d = dict(src_dict)

        def _parse_order(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        order = _parse_order(d.pop("order", UNSET))

        def _parse_step_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        step_type = _parse_step_type(d.pop("stepType", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        def _parse_started_utc(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        started_utc = _parse_started_utc(d.pop("startedUtc", UNSET))

        def _parse_completed_utc(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completed_utc = _parse_completed_utc(d.pop("completedUtc", UNSET))

        def _parse_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        duration_ms = _parse_duration_ms(d.pop("durationMs", UNSET))

        def _parse_duration_human(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        duration_human = _parse_duration_human(d.pop("durationHuman", UNSET))

        def _parse_stats(data: object) -> ExecutionStepStatsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                stats_type_0 = ExecutionStepStatsType0.from_dict(data)

                return stats_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExecutionStepStatsType0 | None | Unset, data)

        stats = _parse_stats(d.pop("stats", UNSET))

        execution_step = cls(
            order=order,
            step_type=step_type,
            status=status,
            version=version,
            started_utc=started_utc,
            completed_utc=completed_utc,
            duration_ms=duration_ms,
            duration_human=duration_human,
            stats=stats,
        )

        execution_step.additional_properties = d
        return execution_step

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
