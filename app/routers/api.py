from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/data")

class DataItem(BaseModel):
    name: str
    value: int

@router.get("/")
async def get_data():
    return {"message": "Data retrieved", "data": [{"name": "test", "value": 1}]}

@router.post("/")
async def post_data(item: DataItem):
    return {"message": "Data processed", "received": item}