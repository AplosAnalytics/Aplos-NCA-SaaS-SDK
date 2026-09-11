from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.user_upsert_request_status import UserUpsertRequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpsertRequest")


@_attrs_define
class UserUpsertRequest:
    """Request body to create or update a user. On create, email is required; on update, only the provided fields are
    changed.

        Attributes:
            email (str | Unset):
            first_name (str | Unset):
            last_name (str | Unset):
            roles (list[str] | Unset):  Example: ['tenant_user'].
            avatar (str | Unset):
            status (UserUpsertRequestStatus | Unset):
    """

    email: str | Unset = UNSET
    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    roles: list[str] | Unset = UNSET
    avatar: str | Unset = UNSET
    status: UserUpsertRequestStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        roles: list[str] | Unset = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        avatar = self.avatar

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if roles is not UNSET:
            field_dict["roles"] = roles
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        email = d.pop("email", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        roles = cast(list[str], d.pop("roles", UNSET))

        avatar = d.pop("avatar", UNSET)

        _status = d.pop("status", UNSET)
        status: UserUpsertRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UserUpsertRequestStatus(_status)

        user_upsert_request = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            roles=roles,
            avatar=avatar,
            status=status,
        )

        user_upsert_request.additional_properties = d
        return user_upsert_request

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
