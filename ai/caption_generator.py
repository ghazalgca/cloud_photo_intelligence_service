from google import genai
from google.genai import types
import json
from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "caption": types.Schema(
            type=types.Type.STRING,
        ),
        "tags": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
        )
    },
    required=["caption", "tags"]
)

config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=schema
)

def generate_caption_and_tags(filepath):

    file = client.files.upload(file=filepath)

    response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=[file, "Generate a short caption and at least 5 tags for this image."],
    config=config,
)

    try:
        data = json.loads(response.text)

        caption = data.get("caption")
        tags = data.get("tags") 

    except json.JSONDecodeError:
        tags = []
        caption = ''

    return caption, tags