from pydantic import BaseModel
from typing import List, Optional

class PhotoMetadata(BaseModel):
    id: str
    filename: str
    upload_time: str
    status: str
    tags: Optional[List[str]]
    caption: Optional[str]
