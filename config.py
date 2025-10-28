import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = "./data/uploads"
PHOTOS_DIR = "./data/photos"
METADATA_DIR = "./data/metadata"
MOODBOARD_DIR = "./data/moodboards"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)
os.makedirs(MOODBOARD_DIR, exist_ok=True)

QDRANT_URL=os.getenv("QDRANT_URL")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = "images"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "clip-ViT-B-32"