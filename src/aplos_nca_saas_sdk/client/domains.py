"""Domain namespaces for the AplosClient facade.

Each namespace exposes curated, ergonomic method names over the generated
per-operation functions. Session tenant_id / user_id are auto-filled; callers
may override by passing them explicitly. Every method returns the unwrapped
`data` (typed entity or list payload) and raises AplosApiError on API errors.

This module wires a representative, high-value subset of the 75 operations
(users, tenants, subscriptions, workflow/executions). The pattern is uniform
and extends to the remaining domains (file-system, report-templates,
audit-logs, feature-flags, metrics, validations, warm-up, maintenance,
site-messages) by adding namespaces the same way.
"""

from __future__ import annotations

from typing import Any, Optional

from aplos_nca_saas_sdk._generated.api.subscriptions import (
    get_tenant_subscription_active_get,
    get_tenant_subscription_get,
    get_tenant_subscriptions_get,
)
from aplos_nca_saas_sdk._generated.api.tenants import (
    get_tenant_get,
    list_tenant_get,
    upsert_tenant_post,
)
from aplos_nca_saas_sdk._generated.api.users import (
    delete_user_delete,
    get_user_get,
    list_users_get,
    upsert_users_post,
)
from aplos_nca_saas_sdk._generated.api.workflow import (
    workflow_get_history_get,
    workflow_get_lineage_get,
    workflow_get_root_get,
    workflow_get_status_get,
)
from aplos_nca_saas_sdk._generated.models.tenant_upsert_request import TenantUpsertRequest
from aplos_nca_saas_sdk._generated.models.user_upsert_request import UserUpsertRequest
from aplos_nca_saas_sdk.client._base import _DomainClient


class UsersClient(_DomainClient):
    """Operations under /v3/tenants/{tenant-id}/users."""

    def get(self, user_id: str, *, tenant_id: Optional[str] = None) -> Any:
        """Get a single user by id."""
        return self._call(
            get_user_get.sync,
            tenant_id=tenant_id or self._tenant_id,
            user_id=user_id,
        )

    def list(self, *, tenant_id: Optional[str] = None) -> Any:
        """List users in the tenant (pagination envelope with `users`)."""
        return self._call(
            list_users_get.sync,
            tenant_id=tenant_id or self._tenant_id,
        )

    def upsert(self, body: UserUpsertRequest, *, tenant_id: Optional[str] = None) -> Any:
        """Create or update a user."""
        return self._call(
            upsert_users_post.sync,
            tenant_id=tenant_id or self._tenant_id,
            body=body,
        )

    def delete(self, user_id: str, *, tenant_id: Optional[str] = None) -> Any:
        """Delete a user."""
        return self._call(
            delete_user_delete.sync,
            tenant_id=tenant_id or self._tenant_id,
            user_id=user_id,
        )


class TenantsClient(_DomainClient):
    """Operations under /v3/tenants."""

    def get(self, tenant_id: Optional[str] = None) -> Any:
        """Get a single tenant (defaults to the session tenant)."""
        return self._call(get_tenant_get.sync, tenant_id=tenant_id or self._tenant_id)

    def list(self) -> Any:
        """List tenants (pagination envelope with `tenants`)."""
        return self._call(list_tenant_get.sync)

    def upsert(self, body: TenantUpsertRequest, *, tenant_id: Optional[str] = None) -> Any:
        """Create or update a tenant."""
        return self._call(
            upsert_tenant_post.sync,
            tenant_id=tenant_id or self._tenant_id,
            body=body,
        )


class SubscriptionsClient(_DomainClient):
    """Operations under /v3/tenants/{tenant-id}/subscriptions."""

    def list(self, *, tenant_id: Optional[str] = None) -> Any:
        """List the tenant's subscriptions."""
        return self._call(
            get_tenant_subscriptions_get.sync, tenant_id=tenant_id or self._tenant_id
        )

    def get(self, subscription_id: str, *, tenant_id: Optional[str] = None) -> Any:
        """Get a single subscription by id."""
        return self._call(
            get_tenant_subscription_get.sync,
            tenant_id=tenant_id or self._tenant_id,
            subscription_id=subscription_id,
        )

    def active(self, *, tenant_id: Optional[str] = None) -> Any:
        """Get the tenant's active subscription."""
        return self._call(
            get_tenant_subscription_active_get.sync,
            tenant_id=tenant_id or self._tenant_id,
        )


class WorkflowClient(_DomainClient):
    """Analysis execution operations under /v3/tenants/{t}/users/{u}/executions."""

    def status(
        self,
        execution_id: str,
        *,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Any:
        """Get an execution's current status/summary (typed Execution)."""
        return self._call(
            workflow_get_status_get.sync,
            tenant_id=tenant_id or self._tenant_id,
            user_id=user_id or self._user_id,
            execution_id=execution_id,
        )

    def root(
        self,
        execution_id: str,
        *,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Any:
        """Get the root execution for a given execution."""
        return self._call(
            workflow_get_root_get.sync,
            tenant_id=tenant_id or self._tenant_id,
            user_id=user_id or self._user_id,
            execution_id=execution_id,
        )

    def lineage(
        self,
        execution_id: str,
        *,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Any:
        """Get the execution lineage (ancestor chain)."""
        return self._call(
            workflow_get_lineage_get.sync,
            tenant_id=tenant_id or self._tenant_id,
            user_id=user_id or self._user_id,
            execution_id=execution_id,
        )

    def history(
        self, *, tenant_id: Optional[str] = None, user_id: Optional[str] = None
    ) -> Any:
        """List execution history (pagination envelope with `executions`)."""
        return self._call(
            workflow_get_history_get.sync,
            tenant_id=tenant_id or self._tenant_id,
            user_id=user_id or self._user_id,
        )
