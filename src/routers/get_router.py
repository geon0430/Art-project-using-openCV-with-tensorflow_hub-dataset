from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from typing import List
from utils import get_logger, get_ini_dict, get_db_manager, APIstruct

get_router = APIRouter()

@get_router.get("/list/", response_model=List[APIstruct])
async def get_items(logger=Depends(get_logger), db_manager=Depends(get_db_manager), ini_dict=Depends(get_ini_dict)):
    start_time = datetime.now()
    json_list = []

    devices = await db_manager.get_db()  

    for item in devices:
        json_list_data = {}
        for field in APIstruct.__fields__.keys():
            json_list_data[field] = getattr(item, field)

        transformed_item = APIstruct(**json_list_data)

        json_list.append(transformed_item)

    elapsed_time = (datetime.now() - start_time).total_seconds()

    if elapsed_time > 2.0:
        logger.error("GET Router | ERROR | Time Out Error")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    logger.info("GET Router | JSON Data send successfully")
    return json_list

@get_router.get("/list/{id}", response_model=APIstruct)
async def get_item_by_id(id: int, logger=Depends(get_logger), db_manager=Depends(get_db_manager), ini_dict=Depends(get_ini_dict)):
    start_time = datetime.now()
    devices = await db_manager.get_db() 

    for item in devices:
        if item.id == id:
            logger.info("GET Router | JSON Data send successfully")
            return item
    elapsed_time = (datetime.now() - start_time).total_seconds()

    if elapsed_time > 2.0:
        logger.error("GET Router | Time Out Error")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")

    logger.error(f"GET Router | Item with id {id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
