from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import QDRANT_API_KEY, QDRANT_URL, QDRANT_COLLECTION

client = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY,
)


vector_config = VectorParams(
    size=512, 
    distance=Distance.COSINE
)


if QDRANT_COLLECTION not in [c.name for c in client.get_collections().collections]:
    client.create_collection(
    collection_name= QDRANT_COLLECTION,
    vectors_config=vector_config,
)
