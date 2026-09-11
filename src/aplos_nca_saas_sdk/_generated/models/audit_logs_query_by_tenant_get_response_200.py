from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_logs_query_by_tenant_get_response_200_data import (
        AuditLogsQueryByTenantGetResponse200Data,
    )
    from ..models.success_envelope_diagnostics import SuccessEnvelopeDiagnostics
    from ..models.success_envelope_metadata import SuccessEnvelopeMetadata


T = TypeVar("T", bound="AuditLogsQueryByTenantGetResponse200")


@_attrs_define
class AuditLogsQueryByTenantGetResponse200:
    """
    Attributes:
        success (bool):  Example: True.
        status_code (int):  Example: 200.
        timestamp (datetime.datetime):
        data (AuditLogsQueryByTenantGetResponse200Data | Unset): Operation payload (shape varies by endpoint).
        message (str | Unset):
        metadata (SuccessEnvelopeMetadata | Unset):
        diagnostics (SuccessEnvelopeDiagnostics | Unset):
    """

    success: bool
    status_code: int
    timestamp: datetime.datetime
    data: AuditLogsQueryByTenantGetResponse200Data | Unset = UNSET
    message: str | Unset = UNSET
    metadata: SuccessEnvelopeMetadata | Unset = UNSET
    diagnostics: SuccessEnvelopeDiagnostics | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        status_code = self.status_code

        timestamp = self.timestamp.isoformat()

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        message = self.message

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        diagnostics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.diagnostics, Unset):
            diagnostics = self.diagnostics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "statusCode": status_code,
                "timestamp": timestamp,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if message is not UNSET:
            field_dict["message"] = message
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if diagnostics is not UNSET:
            field_dict["diagnostics"] = diagnostics

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_logs_query_by_tenant_get_response_200_data import (
            AuditLogsQueryByTenantGetResponse200Data,
        )
        from ..models.success_envelope_diagnostics import SuccessEnvelopeDiagnostics
        from ..models.success_envelope_metadata import SuccessEnvelopeMetadata

        d = dict(src_dict)
        success = d.pop("success")

        status_code = d.pop("statusCode")

        timestamp = isoparse(d.pop("timestamp"))

        _data = d.pop("data", UNSET)
        data: AuditLogsQueryByTenantGetResponse200Data | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = AuditLogsQueryByTenantGetResponse200Data.from_dict(_data)

        message = d.pop("message", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: SuccessEnvelopeMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SuccessEnvelopeMetadata.from_dict(_metadata)

        _diagnostics = d.pop("diagnostics", UNSET)
        diagnostics: SuccessEnvelopeDiagnostics | Unset
        if isinstance(_diagnostics, Unset):
            diagnostics = UNSET
        else:
            diagnostics = SuccessEnvelopeDiagnostics.from_dict(_diagnostics)

        audit_logs_query_by_tenant_get_response_200 = cls(
            success=success,
            status_code=status_code,
            timestamp=timestamp,
            data=data,
            message=message,
            metadata=metadata,
            diagnostics=diagnostics,
        )

        audit_logs_query_by_tenant_get_response_200.additional_properties = d
        return audit_logs_query_by_tenant_get_response_200

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
