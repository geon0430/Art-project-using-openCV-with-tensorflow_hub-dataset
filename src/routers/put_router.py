from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from utils import get_logger, get_ini_dict, get_db_manager, APIstruct

put_router = APIRouter()

@put_router.put("/list/{id}", response_model=APIstruct)
async def PUT_Router(id: int, device: APIstruct, logger=Depends(get_logger), db_manager=Depends(get_db_manager), ini_dict=Depends(get_ini_dict)):
    start_time = datetime.now()
    
    devices = await db_manager.get_db() 
    existing_device = next((d for d in devices if d.id == id), None)
    
    if not existing_device:
        logger.error(f"PUT Router | ERROR | No existing device with id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existing device with id: {id}")

    success = await db_manager.update_device(id, device)  
    if not success:
        logger.error(f"PUT Router | ERROR | Failed to update device with id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to update device with id: {id}")

    logger.info(f"PUT Router | Device with id {id} updated successfully")

    elapsed_time = (datetime.now() - start_time).total_seconds()
    if elapsed_time > 2.0:
        logger.error("PUT Router | ERROR | TIMEOUT Result")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    
    logger.info("PUT Router | JSON Data update successfully")
    return device
