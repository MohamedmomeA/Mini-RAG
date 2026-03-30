from .BaseController import BaseController
from fastapi import UploadFile
from models import result_signal
import os
class ProjectController(BaseController):
    # pass

    def __init__(self):
        super().__init__()

    def get_project_path(self, project_ID: str):
        # pass
        proj_dir = os.path.join(
            self.file_dir,
            project_ID
        )


        if not os.path.exists(proj_dir):
            os.makedirs(proj_dir)


        return proj_dir
