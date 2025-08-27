from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# Supported Gemini models
class ModelName(str, Enum):
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"

# Input schema for a query
class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GEMINI_2_0_FLASH_LITE)  # Default to 1.5-flash

# Output schema for an answer
class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

# Metadata for uploaded documents
class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

# Schema for delete file request
class DeleteFileRequest(BaseModel):
    file_id: int