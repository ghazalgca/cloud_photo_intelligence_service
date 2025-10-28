from database import client
from sentence_transformers import SentenceTransformer
from PIL import Image
from ai.caption_generator import generate_caption_and_tags
import asyncio
import os
import json
from qdrant_client.models import PointStruct
from config import PHOTOS_DIR, METADATA_DIR, EMBEDDING_MODEL, QDRANT_COLLECTION

model = SentenceTransformer(EMBEDDING_MODEL)


async def process_photo(photo_id: str, filename: str, metadata):

    filepath = f"{PHOTOS_DIR}/{filename}"

    caption, tags =await asyncio.to_thread(generate_caption_and_tags, filepath)

    image = Image.open(filepath)
    embedding = model.encode(image).tolist()

    client.upsert(
        QDRANT_COLLECTION,
        wait=True,
        points=[
            PointStruct(
            id=photo_id,
            vector=embedding,
            payload={"filename": filename, "tags": tags, "caption": caption}
        )
        ]
    )

    if metadata:
        metadata.update({
            "tags": tags,
            "caption": caption,
            "status": "processed"
        })

    path = os.path.join(METADATA_DIR, photo_id)
    with open(path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

