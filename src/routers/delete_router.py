from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from datetime import datetime
from utils import get_logger, get_ini_dict, get_db_manager, APIstruct

delete_router = APIRouter()

@delete_router.delete("/list/{id}", response_model=List[APIstruct])
async def DELETE_Router(id: int, logger=Depends(get_logger), db_manager=Depends(get_db_manager), ini_dict=Depends(get_ini_dict)):
    start_time = datetime.now()

    success = await db_manager.remove_device(id)  

    if not success:
        logger.error(f"DELETE Router | Item with id {id} not found ")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")

    elapsed_time = (datetime.now() - start_time).total_seconds()
    
    if elapsed_time > 2.0:
        logger.error("DELETE Router | ERROR | Time Out Error")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")

    logger.info(f"DELETE Router | Item with id {id} deleted successfully")
    return await db_manager.get_db() 
