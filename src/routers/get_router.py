from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List
from datetime import datetime
from utils import get_logger, generate_qr_code
import os

get_router = APIRouter()

BASE_PATH = "/ArtMaker_StyleGan_Tensorflow/src/"

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
