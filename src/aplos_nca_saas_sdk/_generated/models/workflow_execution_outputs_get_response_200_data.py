from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file import File


T = TypeVar("T", bound="WorkflowExecutionOutputsGetResponse200Data")


@_attrs_define
class WorkflowExecutionOutputsGetResponse200Data:
    """
    Attributes:
        count (int): Number of items in this page.
        next_key (None | str | Unset): Opaque base64 pagination token; pass as `start_key` on the next request. Null
            when no more pages remain.
        outputs (list[File] | Unset):
    """

    count: int
    next_key: None | str | Unset = UNSET
    outputs: list[File] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        next_key: None | str | Unset
        if isinstance(self.next_key, Unset):
            next_key = UNSET
        else:
            next_key = self.next_key

        outputs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.outputs, Unset):
            outputs = []
            for outputs_item_data in self.outputs:
                outputs_item = outputs_item_data.to_dict()
                outputs.append(outputs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
            }
        )
        if next_key is not UNSET:
            field_dict["nextKey"] = next_key
        if outputs is not UNSET:
            field_dict["outputs"] = outputs

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.file import File

        d = dict(src_dict)
        count = d.pop("count")

        def _parse_next_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_key = _parse_next_key(d.pop("nextKey", UNSET))

        _outputs = d.pop("outputs", UNSET)
        outputs: list[File] | Unset = UNSET
        if _outputs is not UNSET:
            outputs = []
            for outputs_item_data in _outputs:
                outputs_item = File.from_dict(outputs_item_data)

                outputs.append(outputs_item)

        workflow_execution_outputs_get_response_200_data = cls(
            count=count,
            next_key=next_key,
            outputs=outputs,
        )

        workflow_execution_outputs_get_response_200_data.additional_properties = d
        return workflow_execution_outputs_get_response_200_data

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
