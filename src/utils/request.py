from fastapi import HTTPException, status, Request
    
def get_db_manager(request: Request):
    try:
        db_manager = request.app.state.db_manager
        if db_manager is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Manager not initialized")
        return db_manager
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Manager attribute not found in app state")

def get_logger(request: Request):
    try:
        logger = request.app.state.logger
        if logger is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Logger not initialized")
        return logger
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Logger attribute not found in app state")
    
def get_ini_dict(request: Request):
    try:
        ini_dict = request.app.state.ini_dict
        if ini_dict is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ini_dict not initialized")
        return ini_dict
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ini_dict attribute not found in app state")