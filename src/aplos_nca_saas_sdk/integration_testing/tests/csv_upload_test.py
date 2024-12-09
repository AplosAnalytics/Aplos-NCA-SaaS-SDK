


import os
from pathlib import Path

from aplos_nca_saas_sdk.integration_testing.tests.file_upload_tests.file_upload_test_base import FileUploadTestBase



class CSVUploadTest(FileUploadTestBase):
    
    def __init__(self):
        data_file = os.path.join(Path(__file__).parent, "file_upload_tests", "data.csv")
        super().__init__("csv-upload-test", data_file)