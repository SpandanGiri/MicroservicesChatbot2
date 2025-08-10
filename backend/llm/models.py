from pydantic import  BaseModel
from enum import Enum
from datetime import datetime

class ModelName(str,Enum):
    OLLAMA = "llama3.2"

class QueryInput(BaseModel):
    session_id:str
    question:str
    model:ModelName

class QueryResponse(BaseModel):
    session_id:str
    answer:str
    model:ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int

