# app/api/models/example_model.py
from pydantic import BaseModel

class ExampleModel(BaseModel):
    name: str
    description: str
