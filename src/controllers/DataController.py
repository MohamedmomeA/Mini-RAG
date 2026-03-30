from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import result_signal
import re
import os

class DataController(BaseController):
    # pass

    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024

    def validate_file_type(self, uploaded_file: UploadFile):

        if uploaded_file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,result_signal.FILE_TYPE_NOT_SUPPORTED.value

        if uploaded_file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, result_signal.FILE_SIZE_EXCEED_LIMIT.value
        
        return True, result_signal.FILE_VALIDATING_SUCCESS.value


    def generate_unique_filepath(self, org_filename: str, proj_id: str):

        rand_key = self.generate_random_string()

        project_path = ProjectController().get_project_path(project_ID = proj_id)

        cleaned_filename = self.get_cleaned_filename(org_filename = org_filename)

        rand_file_key = rand_key + "_" + cleaned_filename



        new_file_path = os.path.join(
            project_path,
            rand_file_key
        )


        while os.path.exists(new_file_path):
            rand_filename = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                rand_file_key
            )

        return new_file_path, rand_file_key

    def get_cleaned_filename(self, org_filename):

        # remove any special characters, except underscore and .
        cleaned = re.sub(r'[^\w.]', '', org_filename.strip())

        cleaned = cleaned.replace(" ", "_")

        return cleaned