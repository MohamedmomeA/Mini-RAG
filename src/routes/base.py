from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_setting, Settings
import os



base_route = APIRouter(
    prefix="/api/v1"
)

@base_route.get("/")
async def greating(app_settings: Settings = Depends(get_setting)):
    # app_settings = get_setting()
    app_name = app_settings.APP_NAME
    App_Version = app_settings.APP_VERSION

    return {
        "Message": "Hello World",
        "app_name": app_name,
        "App_Version": App_Version,}

