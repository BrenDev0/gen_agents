from pydantic import BaseModel

class GeneralResponse(BaseModel):
    detail: str