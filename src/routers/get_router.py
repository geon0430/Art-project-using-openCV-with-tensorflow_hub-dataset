from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
from utils import get_logger, generate_qr_code

app = FastAPI()

BASE_PATH = "/ArtMaker_StyleGan_Tensorflow/src"
static_dir = os.path.join(BASE_PATH, "saved_images/picture")
if not os.path.isdir(static_dir):
    os.makedirs(static_dir)

app.mount("/static/image/picture", StaticFiles(directory=static_dir), name="picture")

get_router = APIRouter()

@get_router.get("/saved_images/{image_name}")
async def get_result_image(image_name: str, custom_logger=Depends(get_logger)):
    try:
        image_path = os.path.join(BASE_PATH, "saved_images", image_name)
        
        if not os.path.exists(image_path):
            custom_logger.error(f"Image not found: {image_path}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        
        return FileResponse(image_path)
    except Exception as e:
        custom_logger.error(f"Error getting image {image_name}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving image")

@get_router.get("/generate_qr/{filename:path}")
async def generate_qr(filename: str):
    internal_ip = "192.168.10.10"
    port = 12000
    file_url = f"https://{internal_ip}:{port}/download/{filename}"
    qr_code_path = os.path.join(BASE_PATH, "saved_images", f"{os.path.splitext(os.path.basename(filename))[0]}_qr.jpg")

    qr_path = generate_qr_code(file_url, qr_code_path)
    print(file_url)
    relative_qr_path = os.path.relpath(qr_path, BASE_PATH)
    return {"qr_code_path": f"{relative_qr_path}"}

@get_router.get("/api/get_image_paths")
async def get_image_paths():
    image_directory = os.path.join(BASE_PATH, "saved_images/picture")
    try:
        image_files = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
        image_paths = [f"/static/image/picture/{f}" for f in image_files]
        return {"paths": image_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve image paths")

app.include_router(get_router)
