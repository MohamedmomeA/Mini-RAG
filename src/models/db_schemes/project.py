from pydantic import BaseModel, Field, validator
from typing  import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    # _id: Optional[ObjectId]
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    model_config = {"arbitrary_types_allowed": True}

    id: Optional[ObjectId] = Field(None, alias="_id")

    project_id: str = Field(..., min_length=1)

    # @validator('project_id')
    # async def validate_project_id(cls, value):
    #     if not value.isalnum():
    #         raise ValueError("project id must be alphanumeric")
        
    #     return value
    

    # class config:
    #     arbitrary_types_allowed = True

