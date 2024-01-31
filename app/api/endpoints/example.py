<<<<<<< HEAD
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from lib.example import example_function

router = APIRouter()

@router.get('/example', response_class=PlainTextResponse)
async def example_router(message:str):
    return example_function(message)
=======
# app/api/endpoints/example.py
from fastapi import APIRouter, Depends
from app.api.dependencies.example_dependency import example_dependency
from app.api.models.example_model import ExampleModel

router = APIRouter()

@router.get("/example", response_model=ExampleModel)
def get_example(dependency_result: str = Depends(example_dependency)):
    return {"name": "Example", "description": f"This is an example API endpoint. Dependency result: {dependency_result}"}
>>>>>>> f4aedab (240131 feat: middleware dir changed)
