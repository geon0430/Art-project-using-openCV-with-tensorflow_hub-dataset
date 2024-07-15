from datetime import datetime
import shutil
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from utils import get_logger, get_ini_dict, APIstruct
from model import ArtMaker

post_router = APIRouter()

@post_router.post("/predict/", status_code=status.HTTP_200_OK)
async def predict(content: UploadFile = File(...), style: UploadFile = File(...)):
    content_path = "uploads/" + content.filename
    style_path = "uploads/" + style.filename

    with open(content_path, "wb") as buffer:
        shutil.copyfileobj(content.file, buffer)

    with open(style_path, "wb") as buffer:
        shutil.copyfileobj(style.file, buffer)

    ArtMaker.make_art(content_path, style_path, "output.jpg")

    return JSONResponse(status_code=200, content={"detail": "1", "data": "1"})