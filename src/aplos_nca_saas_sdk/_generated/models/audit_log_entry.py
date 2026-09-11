from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_log_entry_new_values import AuditLogEntryNewValues
    from ..models.audit_log_entry_old_values import AuditLogEntryOldValues


T = TypeVar("T", bound="AuditLogEntry")


@_attrs_define
class AuditLogEntry:
    """An immutable audit log entry (21 CFR Part 11 style). Records who did what to which resource, with an optional change
    diff.

        Attributes:
            id (str):
            action (str): CREATE, UPDATE, DELETE, etc. Example: UPDATE.
            resource_type (str):  Example: file.
            resource_id (str):
            actor_tenant_id (str | Unset):
            actor_user_id (str | Unset):
            actor_email (str | Unset):
            actor_name (str | Unset):
            tenant_id (str | Unset): Tenant that owns the affected resource.
            user_id (str | Unset): Owner of the affected resource.
            resource_name (str | Unset):
            resource_class_name (str | Unset):
            old_values (AuditLogEntryOldValues | Unset):
            new_values (AuditLogEntryNewValues | Unset):
            changed_fields (list[str] | Unset):
            ip_address (str | Unset):
            user_agent (str | Unset):
            request_id (str | Unset):
            created_utc_ts (float | None | Unset):
    """

    id: str
    action: str
    resource_type: str
    resource_id: str
    actor_tenant_id: str | Unset = UNSET
    actor_user_id: str | Unset = UNSET
    actor_email: str | Unset = UNSET
    actor_name: str | Unset = UNSET
    tenant_id: str | Unset = UNSET
    user_id: str | Unset = UNSET
    resource_name: str | Unset = UNSET
    resource_class_name: str | Unset = UNSET
    old_values: AuditLogEntryOldValues | Unset = UNSET
    new_values: AuditLogEntryNewValues | Unset = UNSET
    changed_fields: list[str] | Unset = UNSET
    ip_address: str | Unset = UNSET
    user_agent: str | Unset = UNSET
    request_id: str | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        action = self.action

        resource_type = self.resource_type

        resource_id = self.resource_id

        actor_tenant_id = self.actor_tenant_id

        actor_user_id = self.actor_user_id

        actor_email = self.actor_email

        actor_name = self.actor_name

        tenant_id = self.tenant_id

        user_id = self.user_id

        resource_name = self.resource_name

        resource_class_name = self.resource_class_name

        old_values: dict[str, Any] | Unset = UNSET
        if not isinstance(self.old_values, Unset):
            old_values = self.old_values.to_dict()

        new_values: dict[str, Any] | Unset = UNSET
        if not isinstance(self.new_values, Unset):
            new_values = self.new_values.to_dict()

        changed_fields: list[str] | Unset = UNSET
        if not isinstance(self.changed_fields, Unset):
            changed_fields = self.changed_fields

        ip_address = self.ip_address

        user_agent = self.user_agent

        request_id = self.request_id

        created_utc_ts: float | None | Unset
        if isinstance(self.created_utc_ts, Unset):
            created_utc_ts = UNSET
        else:
            created_utc_ts = self.created_utc_ts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "action": action,
                "resourceType": resource_type,
                "resourceId": resource_id,
            }
        )
        if actor_tenant_id is not UNSET:
            field_dict["actorTenantId"] = actor_tenant_id
        if actor_user_id is not UNSET:
            field_dict["actorUserId"] = actor_user_id
        if actor_email is not UNSET:
            field_dict["actorEmail"] = actor_email
        if actor_name is not UNSET:
            field_dict["actorName"] = actor_name
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if resource_name is not UNSET:
            field_dict["resourceName"] = resource_name
        if resource_class_name is not UNSET:
            field_dict["resourceClassName"] = resource_class_name
        if old_values is not UNSET:
            field_dict["oldValues"] = old_values
        if new_values is not UNSET:
            field_dict["newValues"] = new_values
        if changed_fields is not UNSET:
            field_dict["changedFields"] = changed_fields
        if ip_address is not UNSET:
            field_dict["ipAddress"] = ip_address
        if user_agent is not UNSET:
            field_dict["userAgent"] = user_agent
        if request_id is not UNSET:
            field_dict["requestId"] = request_id
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_log_entry_new_values import AuditLogEntryNewValues
        from ..models.audit_log_entry_old_values import AuditLogEntryOldValues

        d = dict(src_dict)
        id = d.pop("id")

        action = d.pop("action")

        resource_type = d.pop("resourceType")

        resource_id = d.pop("resourceId")

        actor_tenant_id = d.pop("actorTenantId", UNSET)

        actor_user_id = d.pop("actorUserId", UNSET)

        actor_email = d.pop("actorEmail", UNSET)

        actor_name = d.pop("actorName", UNSET)

        tenant_id = d.pop("tenantId", UNSET)

        user_id = d.pop("userId", UNSET)

        resource_name = d.pop("resourceName", UNSET)

        resource_class_name = d.pop("resourceClassName", UNSET)

        _old_values = d.pop("oldValues", UNSET)
        old_values: AuditLogEntryOldValues | Unset
        if isinstance(_old_values, Unset):
            old_values = UNSET
        else:
            old_values = AuditLogEntryOldValues.from_dict(_old_values)

        _new_values = d.pop("newValues", UNSET)
        new_values: AuditLogEntryNewValues | Unset
        if isinstance(_new_values, Unset):
            new_values = UNSET
        else:
            new_values = AuditLogEntryNewValues.from_dict(_new_values)

        changed_fields = cast(list[str], d.pop("changedFields", UNSET))

        ip_address = d.pop("ipAddress", UNSET)

        user_agent = d.pop("userAgent", UNSET)

        request_id = d.pop("requestId", UNSET)

        def _parse_created_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        created_utc_ts = _parse_created_utc_ts(d.pop("createdUtcTs", UNSET))

        audit_log_entry = cls(
            id=id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_tenant_id=actor_tenant_id,
            actor_user_id=actor_user_id,
            actor_email=actor_email,
            actor_name=actor_name,
            tenant_id=tenant_id,
            user_id=user_id,
            resource_name=resource_name,
            resource_class_name=resource_class_name,
            old_values=old_values,
            new_values=new_values,
            changed_fields=changed_fields,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            created_utc_ts=created_utc_ts,
        )

        audit_log_entry.additional_properties = d
        return audit_log_entry

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
