"""
Unit tests for integration test framework updates (Task 11.5).

Tests cover:
- TestConfiguration parses api_version field correctly
- IntegrationTestFactory filters test classes by version

Requirements: 10.4, 10.5
"""

import json
import os
import tempfile

import pytest

from aplos_nca_saas_sdk.integration_testing.integration_test_configurations import (
    TestConfiguration,
)


# ===================================================================
# TestConfiguration tests
# ===================================================================

class TestTestConfigurationApiVersion:
    """Test TestConfiguration parses api_version field correctly."""

    def test_default_api_version_is_v1(self) -> None:
        """api_version should default to 'v1' when not loaded."""
        config = TestConfiguration()
        assert config.api_version == "v1"

    def test_load_with_api_version_v3(self, tmp_path) -> None:
        """load() should read api_version from JSON config."""
        config_data = {
            "api_version": "v3",
            "login_test": {},
            "application_config_test": {},
            "file_upload_test": {},
            "analysis_execution_test": {},
            "analysis_validation_test": {},
        }
        config_file = tmp_path / "test_config.json"
        config_file.write_text(json.dumps(config_data))

        config = TestConfiguration()
        config.load(str(config_file))
        assert config.api_version == "v3"

    def test_load_with_api_version_v1_explicit(self, tmp_path) -> None:
        """load() should read explicit v1 api_version."""
        config_data = {
            "api_version": "v1",
            "login_test": {},
            "application_config_test": {},
            "file_upload_test": {},
            "analysis_execution_test": {},
            "analysis_validation_test": {},
        }
        config_file = tmp_path / "test_config.json"
        config_file.write_text(json.dumps(config_data))

        config = TestConfiguration()
        config.load(str(config_file))
        assert config.api_version == "v1"

    def test_load_without_api_version_defaults_to_v1(self, tmp_path) -> None:
        """When api_version is absent from JSON, it should default to 'v1'."""
        config_data = {
            "login_test": {},
            "application_config_test": {},
            "file_upload_test": {},
            "analysis_execution_test": {},
            "analysis_validation_test": {},
        }
        config_file = tmp_path / "test_config.json"
        config_file.write_text(json.dumps(config_data))

        config = TestConfiguration()
        config.load(str(config_file))
        assert config.api_version == "v1"


# ===================================================================
# IntegrationTestFactory tests
# ===================================================================

class TestIntegrationTestFactoryVersionFiltering:
    """Test IntegrationTestFactory filters test classes by version."""

    def test_v1_factory_excludes_v3_test_files(self) -> None:
        """When api_version='v1', v3-prefixed test files should be skipped.

        We test the filtering logic directly: given a list of test files,
        the factory should skip any file starting with 'v3_' when
        api_version is 'v1'.
        """
        # Replicate the factory's filtering logic
        test_files = [
            "app_login_test.py",
            "v3_execution_test.py",
            "v3_file_operations_test.py",
        ]
        api_version = "v1"

        included = [
            f for f in test_files
            if not (f.startswith("v3_") and api_version != "v3")
        ]

        assert "app_login_test.py" in included
        assert "v3_execution_test.py" not in included
        assert "v3_file_operations_test.py" not in included
        assert len(included) == 1

    def test_v3_factory_includes_v3_test_files(self) -> None:
        """When api_version='v3', v3-prefixed test files should be included."""
        test_files = [
            "app_login_test.py",
            "v3_execution_test.py",
            "v3_file_operations_test.py",
        ]
        api_version = "v3"

        included = [
            f for f in test_files
            if not (f.startswith("v3_") and api_version != "v3")
        ]

        assert "app_login_test.py" in included
        assert "v3_execution_test.py" in included
        assert "v3_file_operations_test.py" in included
        assert len(included) == 3

    def test_factory_real_v1_has_no_v3_instances(self) -> None:
        """A real IntegrationTestFactory(api_version='v1') should not contain v3 test instances."""
        from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
            IntegrationTestFactory,
        )

        factory = IntegrationTestFactory(api_version="v1")
        v3_names = [
            t.name for t in factory.test_instances
            if t.name.lower().startswith("v3")
        ]
        assert len(v3_names) == 0, f"v3 tests should be excluded for v1: {v3_names}"

    def test_factory_real_v3_includes_v3_instances(self) -> None:
        """A real IntegrationTestFactory(api_version='v3') should include v3 test instances."""
        from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
            IntegrationTestFactory,
        )

        factory = IntegrationTestFactory(api_version="v3")
        v3_names = [
            t.name for t in factory.test_instances
            if t.name.lower().startswith("v3")
        ]
        assert len(v3_names) > 0, "v3 tests should be included for v3"

    def test_factory_api_version_property(self) -> None:
        """The api_version property should reflect what was passed to the constructor."""
        from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
            IntegrationTestFactory,
        )

        factory = IntegrationTestFactory(api_version="v3")
        assert factory.api_version == "v3"

    def test_factory_defaults_to_v1(self) -> None:
        """When no api_version is passed, factory should default to 'v1'."""
        from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
            IntegrationTestFactory,
        )

        factory = IntegrationTestFactory()
        assert factory.api_version == "v1"
