"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.nca_resources.api_client_factory import ApiClientFactory
from aplos_nca_saas_sdk.nca_resources.v1.endpoint_strategy import V1EndpointStrategy

ApiClientFactory.register("v1", V1EndpointStrategy)
