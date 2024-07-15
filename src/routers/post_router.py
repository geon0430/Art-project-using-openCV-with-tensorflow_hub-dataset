from datetime import datetime
import shutil
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from utils import get_logger, get_ini_dict, APIstruct
from model import ArtMaker
from utils import WebRTC
from aiortc import RTCSessionDescription


post_router = APIRouter()

@post_router.post("/offer/")
async def offer(request: Request):
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
