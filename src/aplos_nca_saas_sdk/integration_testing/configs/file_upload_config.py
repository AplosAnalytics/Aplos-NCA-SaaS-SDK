"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from typing import List, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase
from aplos_nca_saas_sdk.integration_testing.configs.login_config import LoginConfig, LoginConfigs
from aplos_nca_saas_sdk.utilities.environment_services import EnvironmentServices


class FileUploadConfig(ConfigBase):
    """
    File Upload: Defines the login that the application configuration tests will check against

    """

    def __init__(self, login: LoginConfig, filepath: str):
        super().__init__()
        if login is None:
            raise RuntimeError("Login is required")
        self.__login = login
        if filepath is None:
            raise RuntimeError("Filepath is required")
        self.__filepath = filepath

    @property
    def login(self) -> LoginConfig:
        """The users login"""
        return self.__login

    @property
    def filepath(self) -> str:
        """The file path to file being uploaded"""
        path = self.__load_filepath(self.__filepath)

        if not os.path.exists(path):
            raise RuntimeError(f"The Upload File was not found: {path}")

        return path

    def __load_filepath(self, filepath: str) -> str:
        """Load the filepath"""
        if filepath is None:
            raise RuntimeError("Filepath is required")
        elif filepath.startswith("${module}"):
            # find the path
            es: EnvironmentServices = EnvironmentServices()
            root = es.find_module_path()
            filepath = filepath.replace("${module}", root)

        # get the correct os path separator
        filepath = os.path.normpath(filepath)
        return filepath


class FileUploadConfigs(ConfigBase):
    """
    File Uploads: Defines the files that the application file upload tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__fileuploads: List[FileUploadConfig] = []

    @property
    def list(self) -> List[FileUploadConfig]:
        """List the file uploads"""
        return filter(lambda x: x.enabled, self.__fileuploads)

    def add(self, *, filepath: str, login: LoginConfig, enabled: bool = True):
        """Add a file upload"""
        fileupload = FileUploadConfig(login, filepath)
        fileupload.enabled = enabled
        self.__fileuploads.append(fileupload)

    def load(self, test_config: Dict[str, Any]):
        """Load the file uploads from a list of dictionaries"""

        super().load(test_config)
        test_config_login: LoginConfig = LoginConfigs.try_load_login(test_config.get("login", None))
        fileuploads: List[Dict[str, Any]] = test_config.get("files", [])
        login: LoginConfig = None
        for fileupload in fileuploads:
            enabled = bool(fileupload.get("enabled", True))
            if "login" in fileupload:
                login = LoginConfigs.try_load_login(fileupload["login"])
            else:
                login = test_config_login

            self.add(filepath=fileupload["file"], login=login, enabled=enabled)
