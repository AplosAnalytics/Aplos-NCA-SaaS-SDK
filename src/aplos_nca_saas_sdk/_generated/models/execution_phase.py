from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_step import ExecutionStep


T = TypeVar("T", bound="ExecutionPhase")


@_attrs_define
class ExecutionPhase:
    """A single phase within an execution (e.g. nca_analysis, custom_calculations, custom_reports).

    Attributes:
        order (int | None | Unset):
        phase (None | str | Unset):
        status (None | str | Unset):
        version (None | str | Unset):
        started_utc (None | str | Unset):
        completed_utc (None | str | Unset):
        duration_ms (int | None | Unset):
        duration_human (None | str | Unset):
        outputs (list[Any] | Unset):
        versions (list[Any] | Unset):
        steps (list[ExecutionStep] | Unset):
    """

    order: int | None | Unset = UNSET
    phase: None | str | Unset = UNSET
    status: None | str | Unset = UNSET
    version: None | str | Unset = UNSET
    started_utc: None | str | Unset = UNSET
    completed_utc: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    duration_human: None | str | Unset = UNSET
    outputs: list[Any] | Unset = UNSET
    versions: list[Any] | Unset = UNSET
    steps: list[ExecutionStep] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order: int | None | Unset
        if isinstance(self.order, Unset):
            order = UNSET
        else:
            order = self.order

        phase: None | str | Unset
        if isinstance(self.phase, Unset):
            phase = UNSET
        else:
            phase = self.phase

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

        outputs: list[Any] | Unset = UNSET
        if not isinstance(self.outputs, Unset):
            outputs = self.outputs

        versions: list[Any] | Unset = UNSET
        if not isinstance(self.versions, Unset):
            versions = self.versions

        steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if phase is not UNSET:
            field_dict["phase"] = phase
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
        if outputs is not UNSET:
            field_dict["outputs"] = outputs
        if versions is not UNSET:
            field_dict["versions"] = versions
        if steps is not UNSET:
            field_dict["steps"] = steps

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.execution_step import ExecutionStep

        d = dict(src_dict)

        def _parse_order(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        order = _parse_order(d.pop("order", UNSET))

        def _parse_phase(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        phase = _parse_phase(d.pop("phase", UNSET))

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

        outputs = cast(list[Any], d.pop("outputs", UNSET))

        versions = cast(list[Any], d.pop("versions", UNSET))

        _steps = d.pop("steps", UNSET)
        steps: list[ExecutionStep] | Unset = UNSET
        if _steps is not UNSET:
            steps = []
            for steps_item_data in _steps:
                steps_item = ExecutionStep.from_dict(steps_item_data)

                steps.append(steps_item)

        execution_phase = cls(
            order=order,
            phase=phase,
            status=status,
            version=version,
            started_utc=started_utc,
            completed_utc=completed_utc,
            duration_ms=duration_ms,
            duration_human=duration_human,
            outputs=outputs,
            versions=versions,
            steps=steps,
        )

        execution_phase.additional_properties = d
        return execution_phase

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
