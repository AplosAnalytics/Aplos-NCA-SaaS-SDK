"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.nca_resources.api_client_factory import ApiClientFactory
from aplos_nca_saas_sdk.nca_resources.v3.endpoint_strategy import (
    ApiRoutingConfig,
    V3EndpointStrategy,
)

__all__ = ["ApiRoutingConfig", "V3EndpointStrategy"]

ApiClientFactory.register("v3", V3EndpointStrategy)
