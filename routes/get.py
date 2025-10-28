from fastapi import APIRouter, HTTPException
from metdata_model import PhotoMetadata
import os, json
from config import METADATA_DIR

router = APIRouter()


@router.get("/photo/{photo_id}", response_model=PhotoMetadata)
async def get_photo(photo_id: str):

    path = os.path.normpath(os.path.join(os.path.normpath(METADATA_DIR), f"{photo_id}"))

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Photo not found")

    try:
        with open(path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading metadata: {str(e)}")
    
    return metadata
