from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.error_envelope_error import ErrorEnvelopeError


T = TypeVar("T", bound="ErrorEnvelope")


@_attrs_define
class ErrorEnvelope:
    """Standard error envelope returned by all endpoints.

    Attributes:
        error (ErrorEnvelopeError):
        success (bool):
        status_code (int):  Example: 400.
        timestamp (datetime.datetime):
    """

    error: ErrorEnvelopeError
    success: bool
    status_code: int
    timestamp: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        success = self.success

        status_code = self.status_code

        timestamp = self.timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "success": success,
                "statusCode": status_code,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.error_envelope_error import ErrorEnvelopeError

        d = dict(src_dict)
        error = ErrorEnvelopeError.from_dict(d.pop("error"))

        success = d.pop("success")

        status_code = d.pop("statusCode")

        timestamp = isoparse(d.pop("timestamp"))

        error_envelope = cls(
            error=error,
            success=success,
            status_code=status_code,
            timestamp=timestamp,
        )

        error_envelope.additional_properties = d
        return error_envelope

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
