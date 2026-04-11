from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_setting, Settings
import os
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import result_signal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes.data_chunk import DataChunk


logger = logging.getLogger('uvicorn_error')

data_router = APIRouter(
    prefix="/api/v1/data"
)

@data_router.post("/upload/{project_ID}")
async def upload_data(request: Request, project_ID: str, file: UploadFile, 
                    app_settings: Settings = Depends(get_setting)):

    
    project_model = ProjectModel(
         db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
         project_id=project_ID
    )

    # app_settings = get_setting()
    app_name = app_settings.APP_NAME
    App_Version = app_settings.APP_VERSION

    deta_controller = DataController()

    is_valid, response_signal = deta_controller.validate_file_type(uploaded_file=file)

    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": response_signal
            }
        )


    project_dir_path = ProjectController().get_project_path(project_ID = project_ID)

    file_path, file_id = deta_controller.generate_unique_filepath(
        org_filename = file.filename, 
        proj_id = project_ID
    )

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    
    except Exception as e:

        logger.error(f'error while uploading a file: {e}')

        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": result_signal.FILE_UPLOADED_FAILED.value
            }
        )


    return JSONResponse(
            content = {
                "signal": result_signal.FILE_UPLOADED_SUCCESS.value,
                "file_id": file_id,
            }
        )





@data_router.post("/process/{project_ID}")
async def process_endpoint(request: Request, project_ID: str, process_req: ProcessRequest):

    file_id = process_req.file_id

    chunk_size = process_req.chunk_size
    overlap_size = process_req.overlap_size
    overlap_size = process_req.overlap_size
    do_reset = process_req.do_reset

    # return file_id

    project_model = ProjectModel(
         db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
         project_id=project_ID
    )




    process_controller = ProcessController(project_ID = project_ID)

    file_content = process_controller.get_file_content(file_id = file_id)

    file_chunks =  process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size)

    if file_chunks is None or len(file_chunks) == 0:
                return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": result_signal.PROCESSING_FAILED.value
            }
        )

    
    file_chunks_records = [
         DataChunk(
            chunk_text = chunk.page_content,
            chunk_metadata = chunk.metadata,
            chunk_order = i + 1,
            chunk_project_id = project.id
         )
         for i, chunk in enumerate(file_chunks)
    ]

    chunk_model = ChunkModel(
         db_client = request.app.db_client
    )

    if do_reset == 1:
         _ = await chunk_model.delete_chunks_by_project_id(
              project_id = project.id
         )    

    no_chunks = await chunk_model.insert_many_chunks(chunks = file_chunks_records)
    
     
    return JSONResponse(
        content={
            "signal": result_signal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_chunks
        }
    )
