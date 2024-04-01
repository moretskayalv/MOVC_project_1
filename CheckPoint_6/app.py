from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from fastapi import FastAPI, File, UploadFile
from typing import List
from models_utils import classify_image 
from PIL import Image
import io
from prometheus_client import Histogram
from prometheus_client import make_asgi_app

CLASSIFY_IMAGE_HISTOGRAM = Histogram('classify_image_duration_seconds', 'Время, затраченное на classify_image(img) в секундах')
app = FastAPI()

results = {}


@cache(expire=60)
@app.post("/upload-image/")
async def create_upload_file(image: UploadFile = File(...)):
    # Чтение содержимого изображения
    image_contents = await image.read()
    # Преобразование в объект BytesIO
    img = Image.open(io.BytesIO(image_contents))
    #report = classify_image(img)
    with CLASSIFY_IMAGE_HISTOGRAM.time():
        report = classify_image(img)
    results[image.filename] = report
    
    return {"filename": image.filename,"result":report}

@cache(expire=60)
@app.post("/upload-multiple-images/")
async def create_upload_files(images: List[UploadFile] = File(...)):
    results = {}
    for image in images:
        # Чтение содержимого изображения
        image_contents = await image.read()
        # Преобразование в объект BytesIO
        img = Image.open(io.BytesIO(image_contents))
        # Классификация изображения
        report = classify_image(img)
        # Сохранение результата
        results[image.filename] = report
    
    return results

@cache()
@app.get("/results/")
async def get_results():
    return results

@cache(expire=60)
@app.get("/result/{filename}")
async def get_result_by_filename(filename: str):
    result = results.get(filename)
    if result is not None:
        return {"filename": filename, "result": result}
    else:
        return {"error": "Result not found for the specified filename"}

@app.get("/ping")
async def ping():
    return {"status": 200}


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    app.mount("/metrics", make_asgi_app())

