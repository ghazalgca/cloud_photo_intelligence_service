from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from uuid import uuid4
from datetime import datetime
import os, shutil
from ai.image_processing import process_photo  
from metdata_model import PhotoMetadata
from config import UPLOAD_DIR, PHOTOS_DIR

router = APIRouter()

@router.post("/upload", response_model=PhotoMetadata)
async def upload_photo(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):

    photo_id = str(uuid4())
    filename = f"{photo_id}_{file.filename}"
    temp_path = os.path.join(UPLOAD_DIR, filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    path = os.path.join(PHOTOS_DIR, filename)
    shutil.move(temp_path, path)

    metadata = {
        "id": photo_id,
        "filename": filename,
        "upload_time": datetime.now().isoformat(),
        "status": "uploaded",
        "tags": None,
        "caption": None,
    }

    if background_tasks:
        background_tasks.add_task(process_photo, photo_id, filename, metadata)

    return metadata
