from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
from PIL import Image
import math, uuid
from database import client
from ai.image_processing import model 
from config import MOODBOARD_DIR, PHOTOS_DIR, QDRANT_COLLECTION

router = APIRouter()

@router.get("/moodboard")
async def generate_moodboard(q: str = Query(..., description="Text query for moodboard")):

    query_vector = model.encode(q).tolist()

    search_result = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=9,
        score_threshold=0.2 
    )

    if not search_result:
        raise HTTPException(status_code=404, detail="No matching photos found.")

    images = []
    for image in search_result:
        file_name = image.payload.get("filename")
        if not file_name:
            continue
        path = Path(PHOTOS_DIR) / file_name
        if path.exists():
            images.append(Image.open(path))

    if not images:
        raise HTTPException(status_code=404, detail="No valid images found.")

    num_images = len(images)

    cols = math.ceil(math.sqrt(num_images))
    rows = math.ceil(num_images / cols)

    thumb_size = (256, 256)
    canvas_size = (cols * thumb_size[0], rows * thumb_size[1])
    moodboard = Image.new("RGB", canvas_size, color=(240, 240, 240))

    for idx, img in enumerate(images):
        img = img.resize(thumb_size, Image.LANCZOS)
        row, col = divmod(idx, cols)
        x, y = col * thumb_size[0], row * thumb_size[1]
        moodboard.paste(img, (x, y))

    filename = f"moodboard_{uuid.uuid4().hex}.jpg"
    path = Path(MOODBOARD_DIR) / filename
    moodboard.save(path, "JPEG", quality=90)

    return FileResponse(
        path=path,
        media_type="image/jpeg",
        filename=filename
    )
