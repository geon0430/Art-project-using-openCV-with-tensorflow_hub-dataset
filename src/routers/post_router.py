from fastapi import APIRouter, HTTPException, status, Depends, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from utils import get_logger
from fastapi.responses import FileResponse, JSONResponse
import os
from utils import WebRTC, generate_qr_code
from aiortc import RTCSessionDescription
from model import ArtMaker 
from PIL import Image

post_router = APIRouter()

BASE_PATH = "/ArtMaker_StyleGan_Tensorflow/src/"
STYLE_BASE_PATH = "/ArtMaker_StyleGan_Tensorflow/src/web/"

@post_router.post("/offer/")
async def offer(request: Request, logger=Depends(get_logger)):
    try:
        offer = await request.json()
        rtc_offer = RTCSessionDescription(sdp=offer['sdp'], type=offer['type'])
        local_description = await WebRTC.on_offer(rtc_offer, logger)
        if local_description:
            return {"sdp": local_description.sdp, "type": local_description.type}
        else:
            return {"error": "Failed to generate local description"}
    except Exception as e:
        logger.error(f"offer ERROR | {e}")
        return {"error": str(e)}
    
@post_router.post("/save_screenshot/", status_code=status.HTTP_201_CREATED)
async def save_screenshot_endpoint(image: UploadFile = File(...)):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type")

    save_directory = "saved_images"
    os.makedirs(os.path.join(BASE_PATH, save_directory), exist_ok=True)
    save_path = os.path.join(BASE_PATH, save_directory, os.path.splitext(image.filename)[0] + ".jpg")

    try:
        image_data = await image.read()
        with open(save_path, "wb") as buffer:
            buffer.write(image_data)

        if image.content_type != "image/jpeg":
            im = Image.open(save_path)
            rgb_im = im.convert('RGB')
            rgb_im.save(save_path, format='JPEG')

        relative_path = os.path.relpath(save_path, BASE_PATH)
        return {"image_path": relative_path}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save image: {str(e)}")


@post_router.post("/predict/")
async def predict(content_path: str = Form(...), style_path: str = Form(...)):
    try:
        content_abs_path = os.path.join(BASE_PATH, content_path.lstrip('/'))
        style_abs_path = os.path.join(STYLE_BASE_PATH, style_path.lstrip('/'))
        print(f"Received content path: {content_abs_path}, style path: {style_abs_path}") 

        if not os.path.exists(content_abs_path) or not os.path.exists(style_abs_path):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or both image paths are invalid")

        art_maker = ArtMaker()
        output_path = art_maker.make_art(content_abs_path, style_abs_path)

        filename = os.path.basename(output_path)
        return {"result_image_filename": filename}
    except Exception as e:
        print(f"Error in predict: {e}")  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process images: {str(e)}")


    
@post_router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(BASE_PATH, "saved_images", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='image/jpeg', filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")