from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.queue_accepted_response_status import QueueAcceptedResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueueAcceptedResponse")


@_attrs_define
class QueueAcceptedResponse:
    """Acknowledgement that an analysis was accepted onto the workflow queue. `status` is `queued` normally, or `throttled`
    when admission delayed it (with `delaySeconds`).

        Attributes:
            execution_id (str):
            status (QueueAcceptedResponseStatus):  Example: queued.
            message (str | Unset):
            delay_seconds (int | Unset): Present only when status is throttled.
    """

    execution_id: str
    status: QueueAcceptedResponseStatus
    message: str | Unset = UNSET
    delay_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_id = self.execution_id

        status = self.status.value

        message = self.message

        delay_seconds = self.delay_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "executionId": execution_id,
                "status": status,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if delay_seconds is not UNSET:
            field_dict["delaySeconds"] = delay_seconds

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        execution_id = d.pop("executionId")

        status = QueueAcceptedResponseStatus(d.pop("status"))

        message = d.pop("message", UNSET)

        delay_seconds = d.pop("delaySeconds", UNSET)

        queue_accepted_response = cls(
            execution_id=execution_id,
            status=status,
            message=message,
            delay_seconds=delay_seconds,
        )

        queue_accepted_response.additional_properties = d
        return queue_accepted_response

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
