# app/api/dependencies/example_dependency.py
from fastapi import Depends

def get_example_dependency():
    return "This is an example dependency"

example_dependency = Depends(get_example_dependency)
