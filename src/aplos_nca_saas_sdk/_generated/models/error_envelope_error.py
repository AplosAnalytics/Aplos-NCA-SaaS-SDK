from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_envelope_error_details_type_0 import (
        ErrorEnvelopeErrorDetailsType0,
    )


T = TypeVar("T", bound="ErrorEnvelopeError")


@_attrs_define
class ErrorEnvelopeError:
    """
    Attributes:
        message (str):
        code (str):
        details (ErrorEnvelopeErrorDetailsType0 | None | Unset):
    """

    message: str
    code: str
    details: ErrorEnvelopeErrorDetailsType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.error_envelope_error_details_type_0 import (
            ErrorEnvelopeErrorDetailsType0,
        )

        message = self.message

        code = self.code

        details: dict[str, Any] | None | Unset
        if isinstance(self.details, Unset):
            details = UNSET
        elif isinstance(self.details, ErrorEnvelopeErrorDetailsType0):
            details = self.details.to_dict()
        else:
            details = self.details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "code": code,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.error_envelope_error_details_type_0 import (
            ErrorEnvelopeErrorDetailsType0,
        )

        d = dict(src_dict)
        message = d.pop("message")

        code = d.pop("code")

        def _parse_details(
            data: object,
        ) -> ErrorEnvelopeErrorDetailsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                details_type_0 = ErrorEnvelopeErrorDetailsType0.from_dict(data)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ErrorEnvelopeErrorDetailsType0 | None | Unset, data)

        details = _parse_details(d.pop("details", UNSET))

        error_envelope_error = cls(
            message=message,
            code=code,
            details=details,
        )

        error_envelope_error.additional_properties = d
        return error_envelope_error

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
