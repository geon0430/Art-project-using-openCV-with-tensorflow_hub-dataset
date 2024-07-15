from fastapi import FastAPI
import uvicorn
from utils import setup_logger, ConfigManager
from routers import root, post_router, get_router, delete_router, put_router
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="/Art-project-using-openCV-tensorflow/src/web/static"), name="static")
app.include_router(root)
app.include_router(post_router)
app.include_router(get_router)
app.include_router(delete_router)
app.include_router(put_router)


async def startup_event():
    ini_path = "/Art-project-using-openCV-tensorflow/src/config.ini"
    config = ConfigManager(ini_path)
    ini_dict = config.get_config_dict()
    logger = setup_logger(ini_dict)
    
    logger.info("DASHBOARD STARTED")

    app.state.logger = logger
    app.state.ini_dict = ini_dict

async def shutdown_event():
    await app.state.redis.close()

app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)