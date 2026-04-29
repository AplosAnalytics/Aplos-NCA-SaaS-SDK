# Adding a New API Version

This guide walks through the process of adding support for a new API version
(e.g., v4) to the Aplos NCA SaaS SDK. The SDK uses a **strategy pattern** with
a **factory registry** so that new versions slot in without touching existing
version implementations.

## Overview

Every API version is represented by a *strategy class* that conforms to the
`EndpointStrategy` protocol. The `ApiClientFactory` maintains a registry of
version strings → strategy classes. Adding a version means:

1. Create a new package under `nca_resources/vN/`.
2. Implement a strategy class that satisfies `EndpointStrategy`.
3. Register the strategy with `ApiClientFactory` in the package's `__init__.py`.
4. Add integration tests.

The rest of the SDK (base classes, resource classes, router) picks up the new
version automatically.

---

## Step 1 — Create the version package

Create a directory for the new version inside `src/aplos_nca_saas_sdk/nca_resources/`.
Follow the existing convention used by `v1/` and `v3/`:

```
src/aplos_nca_saas_sdk/nca_resources/
├── v1/
│   ├── __init__.py
│   └── endpoint_strategy.py
├── v3/
│   ├── __init__.py
│   ├── endpoint_strategy.py
│   └── diagnostic_envelope.py
└── v4/                          # ← new
    ├── __init__.py
    └── endpoint_strategy.py
```

The `__init__.py` is where registration happens (Step 3). Any version-specific
helpers (response handlers, data models, etc.) live alongside the strategy in
the same package.

---

## Step 2 — Implement the `EndpointStrategy` protocol

The protocol is defined in
`nca_resources/endpoint_strategy.py`:

```python
# nca_resources/endpoint_strategy.py  (do NOT modify — shown for reference)
from typing import Any, Protocol


class EndpointStrategy(Protocol):
    def get_endpoint_url(
        self,
        operation: str,
        *,
        host: str,
        tenant_id: str | None = None,
        user_id: str | None = None,
        resource_id: str | None = None,
        sub_resource: str | None = None,
    ) -> str: ...

    def process_response(self, response_data: dict[str, Any]) -> dict[str, Any]: ...

    @property
    def version(self) -> str: ...
```

Your new strategy must implement all three members. Here is a minimal skeleton
for a hypothetical **v4**:

```python
# nca_resources/v4/endpoint_strategy.py
"""V4 endpoint strategy."""

from typing import Any


class V4EndpointStrategy:
    """V4 endpoint strategy with <describe what v4 changes>."""

    OPERATIONS: dict[str, str] = {
        # Map every logical operation to its v4 URL template.
        # Use {tenant_id}, {user_id}, {resource_id}, {sub_resource} placeholders.
        "app_configuration": "/v4/app/configuration",
        "tenant": "/v4/tenants/{tenant_id}",
        "user": "/v4/tenants/{tenant_id}/users/{user_id}",
        "executions": "/v4/tenants/{tenant_id}/users/{user_id}/nca/executions",
        "execution": "/v4/tenants/{tenant_id}/users/{user_id}/nca/executions/{resource_id}",
        # ... add all operations supported by v4
    }

    def __init__(self, **kwargs: Any) -> None:
        # Accept and store any version-specific configuration.
        # For example, v3 accepts an `api_routing` kwarg here.
        pass

    @property
    def version(self) -> str:
        return "v4"

    def get_endpoint_url(
        self,
        operation: str,
        *,
        host: str,
        tenant_id: str | None = None,
        user_id: str | None = None,
        resource_id: str | None = None,
        sub_resource: str | None = None,
    ) -> str:
        template = self.OPERATIONS[operation]
        url = f"https://{host}{template}"
        return url.format(
            tenant_id=tenant_id,
            user_id=user_id,
            resource_id=resource_id,
            sub_resource=sub_resource,
        )

    def process_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        # Transform the raw API response before returning it to consumers.
        # V1 returns data as-is; V3 unwraps a diagnostic envelope.
        # Implement whatever v4 requires here.
        return response_data
```

### Key points

- `OPERATIONS` maps logical operation names (e.g., `"executions"`,
  `"file_download_url"`) to URL path templates. Existing operations should keep
  the same logical names so the resource classes (`NCAAnalysis`, `NCAFileUpload`,
  etc.) work without changes.
- `get_endpoint_url` formats the template with the provided IDs and host.
- `process_response` is called on every API response. Use it for envelope
  unwrapping, field renaming, or any version-specific response transformation.
- The `version` property returns the version string (e.g., `"v4"`).

### Reference implementations

| Version | File | Notes |
|---------|------|-------|
| v1 | `nca_resources/v1/endpoint_strategy.py` | Unversioned paths, passthrough responses |
| v3 | `nca_resources/v3/endpoint_strategy.py` | `/v3/` prefix, domain routing, diagnostic envelope unwrapping |

---

## Step 3 — Register with `ApiClientFactory`

The factory lives in `nca_resources/api_client_factory.py`. Registration is a
single `register()` call, and it belongs in your package's `__init__.py`:

```python
# nca_resources/v4/__init__.py
"""V4 API version package."""

from aplos_nca_saas_sdk.nca_resources.api_client_factory import ApiClientFactory
from aplos_nca_saas_sdk.nca_resources.v4.endpoint_strategy import V4EndpointStrategy

__all__ = ["V4EndpointStrategy"]

ApiClientFactory.register("v4", V4EndpointStrategy)
```

That's it. Once this module is imported, `ApiClientFactory.create("v4")` will
return a `V4EndpointStrategy` instance. The SDK's `__init__.py` chain already
imports the `nca_resources` package, which in turn imports each version
sub-package — so registration happens at import time.

> **Important:** Make sure the parent `nca_resources/__init__.py` imports your
> new version package so that registration runs automatically:
>
> ```python
> # nca_resources/__init__.py  (add this line)
> import aplos_nca_saas_sdk.nca_resources.v4  # noqa: F401
> ```

### How the factory works

```python
# nca_resources/api_client_factory.py  (simplified — shown for reference)
class ApiClientFactory:
    _registry: dict[str, type[EndpointStrategy]] = {}

    @classmethod
    def register(cls, version: str, strategy_class: type[EndpointStrategy]) -> None:
        cls._registry[version] = strategy_class

    @classmethod
    def create(cls, version: str | None = None, **kwargs: Any) -> EndpointStrategy:
        resolved = version or os.getenv("APLOS_API_VERSION", "v1")
        if resolved not in cls._registry:
            supported = ", ".join(sorted(cls._registry.keys()))
            raise ValueError(
                f"Unsupported api_version '{resolved}'. Supported versions: {supported}"
            )
        return cls._registry[resolved](**kwargs)
```

- `register()` adds the mapping; no existing code is modified.
- `create()` resolves the version (explicit arg → env var → `"v1"` default),
  looks it up, and instantiates the strategy, forwarding any `**kwargs`.

---

## Step 4 — Add integration tests

Integration tests live in `src/aplos_nca_saas_sdk/integration_testing/tests/`.
Create test files prefixed with `v4_` so the `IntegrationTestFactory` can filter
them by version:

```
integration_testing/tests/
├── app_configuration_test.py          # existing v1
├── v3_execution_test.py               # existing v3
├── v4_execution_test.py               # ← new
└── v4_<feature>_test.py               # ← new
```

Each test class should extend `IntegrationTestBase` and exercise the v4
endpoints against a live (or mocked) API:

```python
# integration_testing/tests/v4_execution_test.py
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class V4ExecutionTest(IntegrationTestBase):
    """Integration tests for v4 execution operations."""

    def run_tests(self) -> None:
        # Use self.host / self.authenticator to make real API calls
        # and assert expected behavior.
        pass
```

The `IntegrationTestFactory` filters test classes by the `api_version` in
`TestConfiguration` — classes prefixed with `v4_` will only run when
`api_version == "v4"`.

---

## Module organization conventions

```
src/aplos_nca_saas_sdk/
└── nca_resources/
    ├── __init__.py                  # imports v1, v3, v4 packages
    ├── endpoint_strategy.py         # EndpointStrategy Protocol (shared)
    ├── api_client_factory.py        # ApiClientFactory (shared)
    ├── api_version_router.py        # ApiVersionRouter (shared)
    ├── _api_base.py                 # NCAApiBaseClass (shared)
    ├── nca_analysis.py              # resource class (version-agnostic)
    ├── nca_file_upload.py           # resource class (version-agnostic)
    ├── nca_file_download.py         # resource class (version-agnostic)
    ├── nca_validations.py           # resource class (version-agnostic)
    ├── v1/
    │   ├── __init__.py              # registers V1EndpointStrategy
    │   └── endpoint_strategy.py     # V1EndpointStrategy
    ├── v3/
    │   ├── __init__.py              # registers V3EndpointStrategy
    │   ├── endpoint_strategy.py     # V3EndpointStrategy + ApiRoutingConfig
    │   └── diagnostic_envelope.py   # DiagnosticEnvelopeHandler
    └── v4/                          # new version follows same layout
        ├── __init__.py              # registers V4EndpointStrategy
        ├── endpoint_strategy.py     # V4EndpointStrategy
        └── <helpers>.py             # any version-specific helpers
```

### Rules of thumb

- **Shared code** (protocol, factory, router, base class) stays in
  `nca_resources/` at the top level.
- **Version-specific code** goes in `nca_resources/vN/`. Never import
  version-specific modules from another version's package.
- **Registration** always happens in `vN/__init__.py` via
  `ApiClientFactory.register()`.
- **Resource classes** (`NCAAnalysis`, `NCAFileUpload`, etc.) remain
  version-agnostic. They delegate to `self.router.strategy` for URL
  construction and response processing.
- **Operation names** should be consistent across versions so resource classes
  don't need version-specific branching. If v4 renames an operation, add the
  new name to the `OPERATIONS` dict and update the resource class call site.

---

## Checklist

- [ ] Created `nca_resources/v4/` package with `__init__.py`
- [ ] Implemented `V4EndpointStrategy` conforming to `EndpointStrategy`
- [ ] Registered strategy via `ApiClientFactory.register("v4", V4EndpointStrategy)`
- [ ] Ensured `nca_resources/__init__.py` imports the new package
- [ ] Added integration tests in `integration_testing/tests/v4_*.py`
- [ ] Verified `ApiClientFactory.create("v4")` returns the new strategy
- [ ] Ran the full test suite to confirm no regressions
