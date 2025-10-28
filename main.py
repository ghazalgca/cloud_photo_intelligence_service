from fastapi import FastAPI
from routes import upload, get, search, moodboard

app = FastAPI()

app.include_router(upload.router)
app.include_router(get.router)
app.include_router(search.router)
app.include_router(moodboard.router)
