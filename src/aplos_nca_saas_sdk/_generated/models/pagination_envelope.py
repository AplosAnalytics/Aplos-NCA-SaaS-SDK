from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaginationEnvelope")


@_attrs_define
class PaginationEnvelope:
    """Standard list/collection payload. Lives inside the SuccessEnvelope `data`. The item array key is the plural resource
    name (e.g. `users`, `executions`).

        Attributes:
            count (int): Number of items in this page.
            next_key (None | str | Unset): Opaque base64 pagination token; pass as `start_key` on the next request. Null
                when no more pages remain.
    """

    count: int
    next_key: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        next_key: None | str | Unset
        if isinstance(self.next_key, Unset):
            next_key = UNSET
        else:
            next_key = self.next_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
            }
        )
        if next_key is not UNSET:
            field_dict["nextKey"] = next_key

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        count = d.pop("count")

        def _parse_next_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_key = _parse_next_key(d.pop("nextKey", UNSET))

        pagination_envelope = cls(
            count=count,
            next_key=next_key,
        )

        pagination_envelope.additional_properties = d
        return pagination_envelope

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
