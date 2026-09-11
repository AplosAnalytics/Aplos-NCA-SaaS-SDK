from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidationTriggerResponse")


@_attrs_define
class ValidationTriggerResponse:
    """Acknowledgement that a validation workflow was queued.

    Attributes:
        execution_id (str):
        status (str):  Example: queued.
        validation_version (str | Unset):
        message (str | Unset):
    """

    execution_id: str
    status: str
    validation_version: str | Unset = UNSET
    message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_id = self.execution_id

        status = self.status

        validation_version = self.validation_version

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "executionId": execution_id,
                "status": status,
            }
        )
        if validation_version is not UNSET:
            field_dict["validationVersion"] = validation_version
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        execution_id = d.pop("executionId")

        status = d.pop("status")

        validation_version = d.pop("validationVersion", UNSET)

        message = d.pop("message", UNSET)

        validation_trigger_response = cls(
            execution_id=execution_id,
            status=status,
            validation_version=validation_version,
            message=message,
        )

        validation_trigger_response.additional_properties = d
        return validation_trigger_response

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
