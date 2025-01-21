from typing import Any, Dict, List
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase
from aplos_nca_saas_sdk.integration_testing.configs.login_config import LoginConfig, LoginConfigs


class NCAExecutionConfig(ConfigBase):
    """
    NCA Execution Config: Defines an NCA Execution configuration that the application execution tests will check against

    """
    
    def __init__(self,
                 login: LoginConfig, 
                 input_file_path: str, 
                 config_data: str | dict, 
                 meta_data: str | dict | None = None, 
                 output_dir: str | None = None,
                 unzip_after_download: bool = False):
        super().__init__()
    
        if login is None:
            raise RuntimeError("login is required")
        self.__login = login
        
        if input_file_path is None:
            raise RuntimeError("input_file_path is required")
        self.__input_file_path = input_file_path
        
        if config_data is None:
            raise RuntimeError("config_data is required")
        self.__config_data = config_data

        self.__meta_data = meta_data
        self.__output_dir = output_dir
        self.__unzip_after_download = unzip_after_download
        
    @property
    def login(self):
        return self.__login
    
    @property
    def input_file_path(self):
        return self.__input_file_path
        
    @property
    def config_data(self):
        return self.__config_data
    
    @property
    def meta_data(self):
        return self.__meta_data
    
    @property
    def output_dir(self):
        return self.__output_dir
    
    @property
    def unzip_after_download(self):
        return self.__unzip_after_download
    
class NCAExecutionConfigs(ConfigBase):
    """
    NCA Execution Configs: Defines the configurations that the application NCA Engine tests will check against

    """
    
    def __init__(self):
        super().__init__()
        self.__nca_executions: List[NCAExecutionConfig] = []
    
    @property
    def list(self) -> List[NCAExecutionConfig]:
        """List the nca execution configurations"""
        return filter(lambda x: x.enabled, self.__nca_executions)
    
    def add(self, *,
                 login: LoginConfig, 
                 input_file_path: str, 
                 config_data: str | dict, 
                 meta_data: str | dict | None = None,
                 output_dir: str | None = None, 
                 unzip_after_download: bool = False, 
                 enabled: bool = True):
        
        """Add an NCA Execution Config"""
        ncaExcutionConfig = NCAExecutionConfig(login, input_file_path, config_data, meta_data, output_dir, unzip_after_download)
        ncaExcutionConfig.enabled = enabled
        self.__nca_executions.append(ncaExcutionConfig)

    def load(self, test_config: Dict[str, Any]):
        """Loads the NCA Execution configs from a list of dictionaries"""
        
        super().load(test_config)
        
        base_login: LoginConfig = LoginConfigs.try_load_login(test_config.get("login", None))
        base_output_dir: str = test_config.get("output_dir", None)
        analyses: List[Dict[str, Any]] = test_config.get("analyses", [])
        for analysis in analyses:
            enabled = bool(analysis.get("enabled", True))
            
            if "login" in analysis:
                login = LoginConfigs.try_load_login(analysis["login"])
            else:
                login = base_login
                
            if "output_dir" in analysis:
                output_dir = analysis["output_dir"]
            else:
                output_dir = base_output_dir
                
            self.add(login=login, 
                     input_file_path=analysis["file"], 
                     config_data=analysis["config"],
                     meta_data=analysis["meta"],
                     output_dir=output_dir,
                     unzip_after_download=True,
                     enabled=enabled)