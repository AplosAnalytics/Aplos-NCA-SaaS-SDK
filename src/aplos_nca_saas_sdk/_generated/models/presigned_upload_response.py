from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.presigned_upload_response_fields import PresignedUploadResponseFields


T = TypeVar("T", bound="PresignedUploadResponse")


@_attrs_define
class PresignedUploadResponse:
    """A presigned S3 upload target. POST the file to `url` with the given `fields` (S3 POST policy) or PUT to `url`
    depending on method.

        Attributes:
            file_id (str | Unset):
            url (str | Unset):
            fields (PresignedUploadResponseFields | Unset): Form fields to include with an S3 POST upload.
            expires_in (int | Unset): Seconds until the URL expires.
            key (str | Unset): S3 object key the upload targets.
    """

    file_id: str | Unset = UNSET
    url: str | Unset = UNSET
    fields: PresignedUploadResponseFields | Unset = UNSET
    expires_in: int | Unset = UNSET
    key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        url = self.url

        fields: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        expires_in = self.expires_in

        key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file_id is not UNSET:
            field_dict["fileId"] = file_id
        if url is not UNSET:
            field_dict["url"] = url
        if fields is not UNSET:
            field_dict["fields"] = fields
        if expires_in is not UNSET:
            field_dict["expiresIn"] = expires_in
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.presigned_upload_response_fields import (
            PresignedUploadResponseFields,
        )

        d = dict(src_dict)
        file_id = d.pop("fileId", UNSET)

        url = d.pop("url", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: PresignedUploadResponseFields | Unset
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = PresignedUploadResponseFields.from_dict(_fields)

        expires_in = d.pop("expiresIn", UNSET)

        key = d.pop("key", UNSET)

        presigned_upload_response = cls(
            file_id=file_id,
            url=url,
            fields=fields,
            expires_in=expires_in,
            key=key,
        )

        presigned_upload_response.additional_properties = d
        return presigned_upload_response

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
