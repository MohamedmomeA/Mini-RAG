from fastapi import FastAPI, APIRouter 
import os



base_route = APIRouter(
    prefix="/api/v1"
)

@base_route.get("/")
async def greating():
    app_name = os.getenv("APP_NAME")
    App_Version = os.getenv("APP_VERSION")

    return {
        "Message": "Hello World",
        "app_name": app_name,
        "App_Version": App_Version,}

