from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List

class APIstruct(BaseModel):
    picture: str
    painting : str