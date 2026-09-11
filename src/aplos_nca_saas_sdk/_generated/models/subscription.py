from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.subscription_billing_interval import SubscriptionBillingInterval
from ..models.subscription_status import SubscriptionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_metadata import SubscriptionMetadata


T = TypeVar("T", bound="Subscription")


@_attrs_define
class Subscription:
    """A tenant subscription (billing plan + limits). Aplos-specific limits (executions, profiles, seats, storage) are
    stored under `metadata`.

        Attributes:
            id (str):
            tenant_id (str):
            status (SubscriptionStatus):  Example: active.
            plan_id (None | str | Unset):
            plan_code (None | str | Unset):  Example: pro.
            plan_name (None | str | Unset):
            seat_count (int | Unset):  Example: 1.
            active_addons (list[str] | Unset):
            price_cents (int | Unset):  Example: 2999.
            currency (str | Unset):  Example: USD.
            billing_interval (SubscriptionBillingInterval | Unset):  Example: month.
            is_trial (bool | Unset):
            trial_ends_utc_ts (float | None | Unset):
            current_period_start_utc_ts (float | None | Unset):
            current_period_end_utc_ts (float | None | Unset):
            canceled_utc_ts (float | None | Unset):
            cancel_at_period_end (bool | Unset):
            cancellation_reason (None | str | Unset):
            next_billing_utc_ts (float | None | Unset):
            payment_method (None | str | Unset):
            external_subscription_id (None | str | Unset):
            notes (None | str | Unset):
            metadata (SubscriptionMetadata | Unset): Custom key/value store. Aplos platform limits live here.
            created_utc_ts (float | None | Unset):
            updated_utc_ts (float | None | Unset):
    """

    id: str
    tenant_id: str
    status: SubscriptionStatus
    plan_id: None | str | Unset = UNSET
    plan_code: None | str | Unset = UNSET
    plan_name: None | str | Unset = UNSET
    seat_count: int | Unset = UNSET
    active_addons: list[str] | Unset = UNSET
    price_cents: int | Unset = UNSET
    currency: str | Unset = UNSET
    billing_interval: SubscriptionBillingInterval | Unset = UNSET
    is_trial: bool | Unset = UNSET
    trial_ends_utc_ts: float | None | Unset = UNSET
    current_period_start_utc_ts: float | None | Unset = UNSET
    current_period_end_utc_ts: float | None | Unset = UNSET
    canceled_utc_ts: float | None | Unset = UNSET
    cancel_at_period_end: bool | Unset = UNSET
    cancellation_reason: None | str | Unset = UNSET
    next_billing_utc_ts: float | None | Unset = UNSET
    payment_method: None | str | Unset = UNSET
    external_subscription_id: None | str | Unset = UNSET
    notes: None | str | Unset = UNSET
    metadata: SubscriptionMetadata | Unset = UNSET
    created_utc_ts: float | None | Unset = UNSET
    updated_utc_ts: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        status = self.status.value

        plan_id: None | str | Unset
        if isinstance(self.plan_id, Unset):
            plan_id = UNSET
        else:
            plan_id = self.plan_id

        plan_code: None | str | Unset
        if isinstance(self.plan_code, Unset):
            plan_code = UNSET
        else:
            plan_code = self.plan_code

        plan_name: None | str | Unset
        if isinstance(self.plan_name, Unset):
            plan_name = UNSET
        else:
            plan_name = self.plan_name

        seat_count = self.seat_count

        active_addons: list[str] | Unset = UNSET
        if not isinstance(self.active_addons, Unset):
            active_addons = self.active_addons

        price_cents = self.price_cents

        currency = self.currency

        billing_interval: str | Unset = UNSET
        if not isinstance(self.billing_interval, Unset):
            billing_interval = self.billing_interval.value

        is_trial = self.is_trial

        trial_ends_utc_ts: float | None | Unset
        if isinstance(self.trial_ends_utc_ts, Unset):
            trial_ends_utc_ts = UNSET
        else:
            trial_ends_utc_ts = self.trial_ends_utc_ts

        current_period_start_utc_ts: float | None | Unset
        if isinstance(self.current_period_start_utc_ts, Unset):
            current_period_start_utc_ts = UNSET
        else:
            current_period_start_utc_ts = self.current_period_start_utc_ts

        current_period_end_utc_ts: float | None | Unset
        if isinstance(self.current_period_end_utc_ts, Unset):
            current_period_end_utc_ts = UNSET
        else:
            current_period_end_utc_ts = self.current_period_end_utc_ts

        canceled_utc_ts: float | None | Unset
        if isinstance(self.canceled_utc_ts, Unset):
            canceled_utc_ts = UNSET
        else:
            canceled_utc_ts = self.canceled_utc_ts

        cancel_at_period_end = self.cancel_at_period_end

        cancellation_reason: None | str | Unset
        if isinstance(self.cancellation_reason, Unset):
            cancellation_reason = UNSET
        else:
            cancellation_reason = self.cancellation_reason

        next_billing_utc_ts: float | None | Unset
        if isinstance(self.next_billing_utc_ts, Unset):
            next_billing_utc_ts = UNSET
        else:
            next_billing_utc_ts = self.next_billing_utc_ts

        payment_method: None | str | Unset
        if isinstance(self.payment_method, Unset):
            payment_method = UNSET
        else:
            payment_method = self.payment_method

        external_subscription_id: None | str | Unset
        if isinstance(self.external_subscription_id, Unset):
            external_subscription_id = UNSET
        else:
            external_subscription_id = self.external_subscription_id

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

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
                "status": status,
            }
        )
        if plan_id is not UNSET:
            field_dict["planId"] = plan_id
        if plan_code is not UNSET:
            field_dict["planCode"] = plan_code
        if plan_name is not UNSET:
            field_dict["planName"] = plan_name
        if seat_count is not UNSET:
            field_dict["seatCount"] = seat_count
        if active_addons is not UNSET:
            field_dict["activeAddons"] = active_addons
        if price_cents is not UNSET:
            field_dict["priceCents"] = price_cents
        if currency is not UNSET:
            field_dict["currency"] = currency
        if billing_interval is not UNSET:
            field_dict["billingInterval"] = billing_interval
        if is_trial is not UNSET:
            field_dict["isTrial"] = is_trial
        if trial_ends_utc_ts is not UNSET:
            field_dict["trialEndsUtcTs"] = trial_ends_utc_ts
        if current_period_start_utc_ts is not UNSET:
            field_dict["currentPeriodStartUtcTs"] = current_period_start_utc_ts
        if current_period_end_utc_ts is not UNSET:
            field_dict["currentPeriodEndUtcTs"] = current_period_end_utc_ts
        if canceled_utc_ts is not UNSET:
            field_dict["canceledUtcTs"] = canceled_utc_ts
        if cancel_at_period_end is not UNSET:
            field_dict["cancelAtPeriodEnd"] = cancel_at_period_end
        if cancellation_reason is not UNSET:
            field_dict["cancellationReason"] = cancellation_reason
        if next_billing_utc_ts is not UNSET:
            field_dict["nextBillingUtcTs"] = next_billing_utc_ts
        if payment_method is not UNSET:
            field_dict["paymentMethod"] = payment_method
        if external_subscription_id is not UNSET:
            field_dict["externalSubscriptionId"] = external_subscription_id
        if notes is not UNSET:
            field_dict["notes"] = notes
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_utc_ts is not UNSET:
            field_dict["createdUtcTs"] = created_utc_ts
        if updated_utc_ts is not UNSET:
            field_dict["updatedUtcTs"] = updated_utc_ts

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.subscription_metadata import SubscriptionMetadata

        d = dict(src_dict)
        id = d.pop("id")

        tenant_id = d.pop("tenantId")

        status = SubscriptionStatus(d.pop("status"))

        def _parse_plan_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plan_id = _parse_plan_id(d.pop("planId", UNSET))

        def _parse_plan_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plan_code = _parse_plan_code(d.pop("planCode", UNSET))

        def _parse_plan_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plan_name = _parse_plan_name(d.pop("planName", UNSET))

        seat_count = d.pop("seatCount", UNSET)

        active_addons = cast(list[str], d.pop("activeAddons", UNSET))

        price_cents = d.pop("priceCents", UNSET)

        currency = d.pop("currency", UNSET)

        _billing_interval = d.pop("billingInterval", UNSET)
        billing_interval: SubscriptionBillingInterval | Unset
        if isinstance(_billing_interval, Unset):
            billing_interval = UNSET
        else:
            billing_interval = SubscriptionBillingInterval(_billing_interval)

        is_trial = d.pop("isTrial", UNSET)

        def _parse_trial_ends_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        trial_ends_utc_ts = _parse_trial_ends_utc_ts(d.pop("trialEndsUtcTs", UNSET))

        def _parse_current_period_start_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        current_period_start_utc_ts = _parse_current_period_start_utc_ts(
            d.pop("currentPeriodStartUtcTs", UNSET)
        )

        def _parse_current_period_end_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        current_period_end_utc_ts = _parse_current_period_end_utc_ts(
            d.pop("currentPeriodEndUtcTs", UNSET)
        )

        def _parse_canceled_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        canceled_utc_ts = _parse_canceled_utc_ts(d.pop("canceledUtcTs", UNSET))

        cancel_at_period_end = d.pop("cancelAtPeriodEnd", UNSET)

        def _parse_cancellation_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cancellation_reason = _parse_cancellation_reason(
            d.pop("cancellationReason", UNSET)
        )

        def _parse_next_billing_utc_ts(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        next_billing_utc_ts = _parse_next_billing_utc_ts(
            d.pop("nextBillingUtcTs", UNSET)
        )

        def _parse_payment_method(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        payment_method = _parse_payment_method(d.pop("paymentMethod", UNSET))

        def _parse_external_subscription_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_subscription_id = _parse_external_subscription_id(
            d.pop("externalSubscriptionId", UNSET)
        )

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: SubscriptionMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SubscriptionMetadata.from_dict(_metadata)

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

        subscription = cls(
            id=id,
            tenant_id=tenant_id,
            status=status,
            plan_id=plan_id,
            plan_code=plan_code,
            plan_name=plan_name,
            seat_count=seat_count,
            active_addons=active_addons,
            price_cents=price_cents,
            currency=currency,
            billing_interval=billing_interval,
            is_trial=is_trial,
            trial_ends_utc_ts=trial_ends_utc_ts,
            current_period_start_utc_ts=current_period_start_utc_ts,
            current_period_end_utc_ts=current_period_end_utc_ts,
            canceled_utc_ts=canceled_utc_ts,
            cancel_at_period_end=cancel_at_period_end,
            cancellation_reason=cancellation_reason,
            next_billing_utc_ts=next_billing_utc_ts,
            payment_method=payment_method,
            external_subscription_id=external_subscription_id,
            notes=notes,
            metadata=metadata,
            created_utc_ts=created_utc_ts,
            updated_utc_ts=updated_utc_ts,
        )

        subscription.additional_properties = d
        return subscription

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
