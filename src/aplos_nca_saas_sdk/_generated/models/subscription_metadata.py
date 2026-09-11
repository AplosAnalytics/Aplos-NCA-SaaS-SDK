from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionMetadata")


@_attrs_define
class SubscriptionMetadata:
    """Custom key/value store. Aplos platform limits live here.

    Attributes:
        max_executions (int | Unset): 0 = unlimited
        max_profiles (int | Unset):
        max_concurrent_executions (int | Unset): 0 = unlimited
        max_seats (int | Unset): 0 = unlimited
        max_storage_bytes (int | Unset): 0 = unlimited
        download_authorized (bool | Unset):
        restricted_grace_days (int | Unset):
        expired_grace_days (int | Unset):
        payment_grace_days (int | Unset):
    """

    max_executions: int | Unset = UNSET
    max_profiles: int | Unset = UNSET
    max_concurrent_executions: int | Unset = UNSET
    max_seats: int | Unset = UNSET
    max_storage_bytes: int | Unset = UNSET
    download_authorized: bool | Unset = UNSET
    restricted_grace_days: int | Unset = UNSET
    expired_grace_days: int | Unset = UNSET
    payment_grace_days: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_executions = self.max_executions

        max_profiles = self.max_profiles

        max_concurrent_executions = self.max_concurrent_executions

        max_seats = self.max_seats

        max_storage_bytes = self.max_storage_bytes

        download_authorized = self.download_authorized

        restricted_grace_days = self.restricted_grace_days

        expired_grace_days = self.expired_grace_days

        payment_grace_days = self.payment_grace_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_executions is not UNSET:
            field_dict["maxExecutions"] = max_executions
        if max_profiles is not UNSET:
            field_dict["maxProfiles"] = max_profiles
        if max_concurrent_executions is not UNSET:
            field_dict["maxConcurrentExecutions"] = max_concurrent_executions
        if max_seats is not UNSET:
            field_dict["maxSeats"] = max_seats
        if max_storage_bytes is not UNSET:
            field_dict["maxStorageBytes"] = max_storage_bytes
        if download_authorized is not UNSET:
            field_dict["downloadAuthorized"] = download_authorized
        if restricted_grace_days is not UNSET:
            field_dict["restrictedGraceDays"] = restricted_grace_days
        if expired_grace_days is not UNSET:
            field_dict["expiredGraceDays"] = expired_grace_days
        if payment_grace_days is not UNSET:
            field_dict["paymentGraceDays"] = payment_grace_days

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_executions = d.pop("maxExecutions", UNSET)

        max_profiles = d.pop("maxProfiles", UNSET)

        max_concurrent_executions = d.pop("maxConcurrentExecutions", UNSET)

        max_seats = d.pop("maxSeats", UNSET)

        max_storage_bytes = d.pop("maxStorageBytes", UNSET)

        download_authorized = d.pop("downloadAuthorized", UNSET)

        restricted_grace_days = d.pop("restrictedGraceDays", UNSET)

        expired_grace_days = d.pop("expiredGraceDays", UNSET)

        payment_grace_days = d.pop("paymentGraceDays", UNSET)

        subscription_metadata = cls(
            max_executions=max_executions,
            max_profiles=max_profiles,
            max_concurrent_executions=max_concurrent_executions,
            max_seats=max_seats,
            max_storage_bytes=max_storage_bytes,
            download_authorized=download_authorized,
            restricted_grace_days=restricted_grace_days,
            expired_grace_days=expired_grace_days,
            payment_grace_days=payment_grace_days,
        )

        subscription_metadata.additional_properties = d
        return subscription_metadata

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
