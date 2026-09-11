from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_input_type_0 import ExecutionInputType0
    from ..models.execution_phase import ExecutionPhase
    from ..models.execution_progress import ExecutionProgress


T = TypeVar("T", bound="Execution")


@_attrs_define
class Execution:
    """An analysis execution summary. The same shape is returned by the status, root, history, and lineage endpoints
    (history/lineage return arrays of this). Fields are formatted by ExecutionSummaryFormatter.to_api_response.

        Attributes:
            id (str):
            parent_id (None | str | Unset):
            root_id (None | str | Unset):
            name (None | str | Unset):
            execution_type (None | str | Unset):
            workflow_type (None | str | Unset):
            status (None | str | Unset):
            status_message (None | str | Unset):
            error_code (None | str | Unset):
            current_phase (None | str | Unset):
            progress (ExecutionProgress | Unset):
            created_utc (None | str | Unset):
            started_utc (None | str | Unset):
            completed_utc (None | str | Unset):
            duration_ms (int | None | Unset):
            duration_human (None | str | Unset):
            input_ (ExecutionInputType0 | None | Unset): The original analysis input (e.g. fileId, config references).
            phases (list[ExecutionPhase] | Unset):
            package_available (bool | Unset):
            error (Any | Unset): First error, if any (same element as errors[0]).
            errors (list[Any] | Unset):
            warnings (list[Any] | Unset):
            engine_versions (list[Any] | Unset):
            phase_types (list[str] | Unset):
            lifecycle_state (None | str | Unset):  Example: active.
            analysis_engine_version (None | str | Unset):
            children (list[Execution] | Unset): Populated only in tree/lineage views; child executions nested under a root.
    """

    id: str
    parent_id: None | str | Unset = UNSET
    root_id: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    execution_type: None | str | Unset = UNSET
    workflow_type: None | str | Unset = UNSET
    status: None | str | Unset = UNSET
    status_message: None | str | Unset = UNSET
    error_code: None | str | Unset = UNSET
    current_phase: None | str | Unset = UNSET
    progress: ExecutionProgress | Unset = UNSET
    created_utc: None | str | Unset = UNSET
    started_utc: None | str | Unset = UNSET
    completed_utc: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    duration_human: None | str | Unset = UNSET
    input_: ExecutionInputType0 | None | Unset = UNSET
    phases: list[ExecutionPhase] | Unset = UNSET
    package_available: bool | Unset = UNSET
    error: Any | Unset = UNSET
    errors: list[Any] | Unset = UNSET
    warnings: list[Any] | Unset = UNSET
    engine_versions: list[Any] | Unset = UNSET
    phase_types: list[str] | Unset = UNSET
    lifecycle_state: None | str | Unset = UNSET
    analysis_engine_version: None | str | Unset = UNSET
    children: list[Execution] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.execution_input_type_0 import ExecutionInputType0

        id = self.id

        parent_id: None | str | Unset
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        root_id: None | str | Unset
        if isinstance(self.root_id, Unset):
            root_id = UNSET
        else:
            root_id = self.root_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        execution_type: None | str | Unset
        if isinstance(self.execution_type, Unset):
            execution_type = UNSET
        else:
            execution_type = self.execution_type

        workflow_type: None | str | Unset
        if isinstance(self.workflow_type, Unset):
            workflow_type = UNSET
        else:
            workflow_type = self.workflow_type

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        status_message: None | str | Unset
        if isinstance(self.status_message, Unset):
            status_message = UNSET
        else:
            status_message = self.status_message

        error_code: None | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        else:
            error_code = self.error_code

        current_phase: None | str | Unset
        if isinstance(self.current_phase, Unset):
            current_phase = UNSET
        else:
            current_phase = self.current_phase

        progress: dict[str, Any] | Unset = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()

        created_utc: None | str | Unset
        if isinstance(self.created_utc, Unset):
            created_utc = UNSET
        else:
            created_utc = self.created_utc

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

        input_: dict[str, Any] | None | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        elif isinstance(self.input_, ExecutionInputType0):
            input_ = self.input_.to_dict()
        else:
            input_ = self.input_

        phases: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.phases, Unset):
            phases = []
            for phases_item_data in self.phases:
                phases_item = phases_item_data.to_dict()
                phases.append(phases_item)

        package_available = self.package_available

        error = self.error

        errors: list[Any] | Unset = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        warnings: list[Any] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        engine_versions: list[Any] | Unset = UNSET
        if not isinstance(self.engine_versions, Unset):
            engine_versions = self.engine_versions

        phase_types: list[str] | Unset = UNSET
        if not isinstance(self.phase_types, Unset):
            phase_types = self.phase_types

        lifecycle_state: None | str | Unset
        if isinstance(self.lifecycle_state, Unset):
            lifecycle_state = UNSET
        else:
            lifecycle_state = self.lifecycle_state

        analysis_engine_version: None | str | Unset
        if isinstance(self.analysis_engine_version, Unset):
            analysis_engine_version = UNSET
        else:
            analysis_engine_version = self.analysis_engine_version

        children: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if root_id is not UNSET:
            field_dict["rootId"] = root_id
        if name is not UNSET:
            field_dict["name"] = name
        if execution_type is not UNSET:
            field_dict["executionType"] = execution_type
        if workflow_type is not UNSET:
            field_dict["workflowType"] = workflow_type
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if current_phase is not UNSET:
            field_dict["currentPhase"] = current_phase
        if progress is not UNSET:
            field_dict["progress"] = progress
        if created_utc is not UNSET:
            field_dict["createdUtc"] = created_utc
        if started_utc is not UNSET:
            field_dict["startedUtc"] = started_utc
        if completed_utc is not UNSET:
            field_dict["completedUtc"] = completed_utc
        if duration_ms is not UNSET:
            field_dict["durationMs"] = duration_ms
        if duration_human is not UNSET:
            field_dict["durationHuman"] = duration_human
        if input_ is not UNSET:
            field_dict["input"] = input_
        if phases is not UNSET:
            field_dict["phases"] = phases
        if package_available is not UNSET:
            field_dict["packageAvailable"] = package_available
        if error is not UNSET:
            field_dict["error"] = error
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if engine_versions is not UNSET:
            field_dict["engineVersions"] = engine_versions
        if phase_types is not UNSET:
            field_dict["phaseTypes"] = phase_types
        if lifecycle_state is not UNSET:
            field_dict["lifecycleState"] = lifecycle_state
        if analysis_engine_version is not UNSET:
            field_dict["analysisEngineVersion"] = analysis_engine_version
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.execution_input_type_0 import ExecutionInputType0
        from ..models.execution_phase import ExecutionPhase
        from ..models.execution_progress import ExecutionProgress

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_parent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_id = _parse_parent_id(d.pop("parentId", UNSET))

        def _parse_root_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        root_id = _parse_root_id(d.pop("rootId", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_execution_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        execution_type = _parse_execution_type(d.pop("executionType", UNSET))

        def _parse_workflow_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workflow_type = _parse_workflow_type(d.pop("workflowType", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_status_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status_message = _parse_status_message(d.pop("statusMessage", UNSET))

        def _parse_error_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_code = _parse_error_code(d.pop("errorCode", UNSET))

        def _parse_current_phase(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        current_phase = _parse_current_phase(d.pop("currentPhase", UNSET))

        _progress = d.pop("progress", UNSET)
        progress: ExecutionProgress | Unset
        if isinstance(_progress, Unset):
            progress = UNSET
        else:
            progress = ExecutionProgress.from_dict(_progress)

        def _parse_created_utc(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_utc = _parse_created_utc(d.pop("createdUtc", UNSET))

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

        def _parse_input_(data: object) -> ExecutionInputType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_0 = ExecutionInputType0.from_dict(data)

                return input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExecutionInputType0 | None | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        _phases = d.pop("phases", UNSET)
        phases: list[ExecutionPhase] | Unset = UNSET
        if _phases is not UNSET:
            phases = []
            for phases_item_data in _phases:
                phases_item = ExecutionPhase.from_dict(phases_item_data)

                phases.append(phases_item)

        package_available = d.pop("packageAvailable", UNSET)

        error = d.pop("error", UNSET)

        errors = cast(list[Any], d.pop("errors", UNSET))

        warnings = cast(list[Any], d.pop("warnings", UNSET))

        engine_versions = cast(list[Any], d.pop("engineVersions", UNSET))

        phase_types = cast(list[str], d.pop("phaseTypes", UNSET))

        def _parse_lifecycle_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lifecycle_state = _parse_lifecycle_state(d.pop("lifecycleState", UNSET))

        def _parse_analysis_engine_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        analysis_engine_version = _parse_analysis_engine_version(
            d.pop("analysisEngineVersion", UNSET)
        )

        _children = d.pop("children", UNSET)
        children: list[Execution] | Unset = UNSET
        if _children is not UNSET:
            children = []
            for children_item_data in _children:
                children_item = Execution.from_dict(children_item_data)

                children.append(children_item)

        execution = cls(
            id=id,
            parent_id=parent_id,
            root_id=root_id,
            name=name,
            execution_type=execution_type,
            workflow_type=workflow_type,
            status=status,
            status_message=status_message,
            error_code=error_code,
            current_phase=current_phase,
            progress=progress,
            created_utc=created_utc,
            started_utc=started_utc,
            completed_utc=completed_utc,
            duration_ms=duration_ms,
            duration_human=duration_human,
            input_=input_,
            phases=phases,
            package_available=package_available,
            error=error,
            errors=errors,
            warnings=warnings,
            engine_versions=engine_versions,
            phase_types=phase_types,
            lifecycle_state=lifecycle_state,
            analysis_engine_version=analysis_engine_version,
            children=children,
        )

        execution.additional_properties = d
        return execution

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
