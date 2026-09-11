from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_metadata import FileMetadata


T = TypeVar("T", bound="File")


@_attrs_define
class File:
    """File metadata record (the file's bytes live in S3; this is metadata + references).

    Attributes:
        id (str):
        tenant_id (str):
        owner_id (str):
        name (None | str | Unset):
        extension (None | str | Unset):
        mime_type (None | str | Unset):
        content_type (None | str | Unset):
        size (int | Unset): Size in bytes.
        checksum (None | str | Unset):
        directory_id (None | str | Unset):
        virtual_path (None | str | Unset):
        bucket (None | str | Unset):
        key (None | str | Unset):
        version_id (None | str | Unset):
        status (None | str | Unset):
        state (str | Unset):
        lineage (str | Unset):
        root_id (None | str | Unset):
        parent_id (None | str | Unset):
        category (None | str | Unset):
        visibility (str | Unset):
        retention_policy (None | str | Unset):
        is_hidden (bool | Unset):
        description (None | str | Unset):
        metadata (FileMetadata | Unset):
        uploaded_utc_ts (int | None | Unset):
        created_utc_ts (float | None | Unset):
        updated_utc_ts (float | None | Unset):
    """

    id: str
    tenant_id: str
    owner_id: str
    name: None | str | Unset = UNSET
    extension: None | str | Unset = UNSET
    mime_type: None | str | Unset = UNSET
    content_type: None | str | Unset = UNSET
    size: int | Unset = UNSET
    checksum: None | str | Unset = UNSET
    directory_id: None | str | Unset = UNSET
    virtual_path: None | str | Unset = UNSET
    bucket: None | str | Unset = UNSET
    key: None | str | Unset = UNSET
    version_id: None | str | Unset = UNSET
    status: None | str | Unset = UNSET
    state: str | Unset = UNSET
    lineage: str | Unset = UNSET
    root_id: None | str | Unset = UNSET
    parent_id: None | str | Unset = UNSET
    category: None | str | Unset = UNSET
    visibility: str | Unset = UNSET
    retention_policy: None | str | Unset = UNSET
    is_hidden: bool | Unset = UNSET
    description: None | str | Unset = UNSET
    metadata: FileMetadata | Unset = UNSET
    uploaded_utc_ts: int | None | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        owner_id = self.owner_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        extension: None | str | Unset
        if isinstance(self.extension, Unset):
            extension = UNSET
        else:
            extension = self.extension

        mime_type: None | str | Unset
        if isinstance(self.mime_type, Unset):
            mime_type = UNSET
        else:
            mime_type = self.mime_type

        content_type: None | str | Unset
        if isinstance(self.content_type, Unset):
            content_type = UNSET
        else:
            content_type = self.content_type

        size = self.size

        checksum: None | str | Unset
        if isinstance(self.checksum, Unset):
            checksum = UNSET
        else:
            checksum = self.checksum

        directory_id: None | str | Unset
        if isinstance(self.directory_id, Unset):
            directory_id = UNSET
        else:
            directory_id = self.directory_id

        virtual_path: None | str | Unset
        if isinstance(self.virtual_path, Unset):
            virtual_path = UNSET
        else:
            virtual_path = self.virtual_path

        bucket: None | str | Unset
        if isinstance(self.bucket, Unset):
            bucket = UNSET
        else:
            bucket = self.bucket

        key: None | str | Unset
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        version_id: None | str | Unset
        if isinstance(self.version_id, Unset):
            version_id = UNSET
        else:
            version_id = self.version_id

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        state = self.state

        lineage = self.lineage

        root_id: None | str | Unset
        if isinstance(self.root_id, Unset):
            root_id = UNSET
        else:
            root_id = self.root_id

        parent_id: None | str | Unset
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        visibility = self.visibility

        retention_policy: None | str | Unset
        if isinstance(self.retention_policy, Unset):
            retention_policy = UNSET
        else:
            retention_policy = self.retention_policy

        is_hidden = self.is_hidden

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        uploaded_utc_ts: int | None | Unset
        if isinstance(self.uploaded_utc_ts, Unset):
            uploaded_utc_ts = UNSET
        else:
            uploaded_utc_ts = self.uploaded_utc_ts

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
                "ownerId": owner_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if extension is not UNSET:
            field_dict["extension"] = extension
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if size is not UNSET:
            field_dict["size"] = size
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if directory_id is not UNSET:
            field_dict["directoryId"] = directory_id
        if virtual_path is not UNSET:
            field_dict["virtualPath"] = virtual_path
        if bucket is not UNSET:
            field_dict["bucket"] = bucket
        if key is not UNSET:
            field_dict["key"] = key
        if version_id is not UNSET:
            field_dict["versionId"] = version_id
        if status is not UNSET:
            field_dict["status"] = status
        if state is not UNSET:
            field_dict["state"] = state
        if lineage is not UNSET:
            field_dict["lineage"] = lineage
        if root_id is not UNSET:
            field_dict["rootId"] = root_id
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if category is not UNSET:
            field_dict["category"] = category
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if retention_policy is not UNSET:
            field_dict["retentionPolicy"] = retention_policy
        if is_hidden is not UNSET:
            field_dict["isHidden"] = is_hidden
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if uploaded_utc_ts is not UNSET:
            field_dict["uploadedUtcTs"] = uploaded_utc_ts
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.file_metadata import FileMetadata

        d = dict(src_dict)
        id = d.pop("id")

        tenant_id = d.pop("tenantId")

        owner_id = d.pop("ownerId")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_extension(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        extension = _parse_extension(d.pop("extension", UNSET))

        def _parse_mime_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        mime_type = _parse_mime_type(d.pop("mimeType", UNSET))

        def _parse_content_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content_type = _parse_content_type(d.pop("contentType", UNSET))

        size = d.pop("size", UNSET)

        def _parse_checksum(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        checksum = _parse_checksum(d.pop("checksum", UNSET))

        def _parse_directory_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        directory_id = _parse_directory_id(d.pop("directoryId", UNSET))

        def _parse_virtual_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        virtual_path = _parse_virtual_path(d.pop("virtualPath", UNSET))

        def _parse_bucket(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bucket = _parse_bucket(d.pop("bucket", UNSET))

        def _parse_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key = _parse_key(d.pop("key", UNSET))

        def _parse_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        version_id = _parse_version_id(d.pop("versionId", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        state = d.pop("state", UNSET)

        lineage = d.pop("lineage", UNSET)

        def _parse_root_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        root_id = _parse_root_id(d.pop("rootId", UNSET))

        def _parse_parent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_id = _parse_parent_id(d.pop("parentId", UNSET))

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        visibility = d.pop("visibility", UNSET)

        def _parse_retention_policy(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        retention_policy = _parse_retention_policy(d.pop("retentionPolicy", UNSET))

        is_hidden = d.pop("isHidden", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: FileMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = FileMetadata.from_dict(_metadata)

        def _parse_uploaded_utc_ts(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        uploaded_utc_ts = _parse_uploaded_utc_ts(d.pop("uploadedUtcTs", UNSET))

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

        file = cls(
            id=id,
            tenant_id=tenant_id,
            owner_id=owner_id,
            name=name,
            extension=extension,
            mime_type=mime_type,
            content_type=content_type,
            size=size,
            checksum=checksum,
            directory_id=directory_id,
            virtual_path=virtual_path,
            bucket=bucket,
            key=key,
            version_id=version_id,
            status=status,
            state=state,
            lineage=lineage,
            root_id=root_id,
            parent_id=parent_id,
            category=category,
            visibility=visibility,
            retention_policy=retention_policy,
            is_hidden=is_hidden,
            description=description,
            metadata=metadata,
            uploaded_utc_ts=uploaded_utc_ts,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        file.additional_properties = d
        return file

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
