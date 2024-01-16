from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from lib.example import example_function

router = APIRouter()

@router.get('/example', response_class=PlainTextResponse)
async def example_router(message:str):
    return example_function(message)
