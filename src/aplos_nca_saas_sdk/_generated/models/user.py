from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.user_status import UserStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """A user within a tenant.

    Attributes:
        id (str):
        tenant_id (str):
        email (str):
        first_name (None | str | Unset):
        last_name (None | str | Unset):
        full_name (str | Unset):
        roles (list[str] | Unset):  Example: ['tenant_user'].
        primary_role (str | Unset):  Example: tenant_user.
        is_admin (bool | Unset):
        avatar (None | str | Unset):
        identity_provider (str | Unset): Primary identity provider: cognito | google | office365 | facebook | saml
            Example: cognito.
        status (UserStatus | Unset):  Example: active.
        created_utc_ts (float | None | Unset):
        updated_utc_ts (float | None | Unset):
    """

    id: str
    tenant_id: str
    email: str
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    full_name: str | Unset = UNSET
    roles: list[str] | Unset = UNSET
    primary_role: str | Unset = UNSET
    is_admin: bool | Unset = UNSET
    avatar: None | str | Unset = UNSET
    identity_provider: str | Unset = UNSET
    status: UserStatus | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        email = self.email

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        full_name = self.full_name

        roles: list[str] | Unset = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        primary_role = self.primary_role

        is_admin = self.is_admin

        avatar: None | str | Unset
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        identity_provider = self.identity_provider

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        created_utc_ts: float | None | Unset
        if isinstance(self.created_utc_ts, Unset):
            created_utc_ts = UNSET
        else:
            created_utc_ts = self.created_utc_ts

        updated_utc_ts: float | None | Unset
        if isinstance(self.updated_utc_ts, Unset):
            updated_utc_ts = UNSET
        else:
            updated_utc_ts = self.updated_utc_ts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tenantId": tenant_id,
                "email": email,
            }
        )
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if roles is not UNSET:
            field_dict["roles"] = roles
        if primary_role is not UNSET:
            field_dict["primaryRole"] = primary_role
        if is_admin is not UNSET:
            field_dict["isAdmin"] = is_admin
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if identity_provider is not UNSET:
            field_dict["identityProvider"] = identity_provider
        if status is not UNSET:
            field_dict["status"] = status
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        tenant_id = d.pop("tenantId")

        email = d.pop("email")

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("firstName", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("lastName", UNSET))

        full_name = d.pop("fullName", UNSET)

        roles = cast(list[str], d.pop("roles", UNSET))

        primary_role = d.pop("primaryRole", UNSET)

        is_admin = d.pop("isAdmin", UNSET)

        def _parse_avatar(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        identity_provider = d.pop("identityProvider", UNSET)

        _status = d.pop("status", UNSET)
        status: UserStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UserStatus(_status)

        def _parse_created_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        created_utc_ts = _parse_created_utc_ts(d.pop("createdUtcTs", UNSET))

        def _parse_updated_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        updated_utc_ts = _parse_updated_utc_ts(d.pop("updatedUtcTs", UNSET))

        user = cls(
            id=id,
            tenant_id=tenant_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            roles=roles,
            primary_role=primary_role,
            is_admin=is_admin,
            avatar=avatar,
            identity_provider=identity_provider,
            status=status,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        user.additional_properties = d
        return user

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
