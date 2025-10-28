from fastapi import APIRouter, HTTPException, Query
from database import client
from ai.image_processing import model
import json, os
from config import METADATA_DIR, QDRANT_COLLECTION


router = APIRouter()

@router.get("/search")
async def search_photos(q: str = Query(..., description="Search query")):
    try:
        query_vector = model.encode(q).tolist()

        results = client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=10,
            score_threshold=0.2
        )

        response = []
        for r in results:
            photo_id = r.payload.get("id") or r.id
            path = os.path.normpath(os.path.join(os.path.normpath(METADATA_DIR), f"{photo_id}"))

            if os.path.exists(path):
                with open(path, "r") as f:
                    metadata = json.load(f)
            else:
                metadata = {"id": photo_id, "note": "Metadata not found"}

            response.append({
                "photo_id": photo_id,
                "score": r.score,
                "metadata": metadata
            })

        return {"query": q, "results": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
