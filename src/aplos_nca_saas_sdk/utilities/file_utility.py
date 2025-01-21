"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os


from aplos_nca_saas_sdk.utilities.environment_services import EnvironmentServices


class FileUtility:
    """General File Utilities"""

    @staticmethod
    def load_filepath(filepath: str) -> str:
        """Load the filepath"""
        if not filepath:
            raise RuntimeError("Filepath is required")
        elif filepath.startswith("${module}"):
            # find the path
            es: EnvironmentServices = EnvironmentServices()
            root = es.find_module_path()
            filepath = filepath.replace("${module}", root)

        # get the correct os path separator
        filepath = os.path.normpath(filepath)
        return filepath
