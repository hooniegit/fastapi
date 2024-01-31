<<<<<<< HEAD
from fastapi import FastAPI
from app.api.endpoints.authentication_endpoints import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
=======
# main.py
from fastapi import FastAPI
from app.middleware.example_middleware import example_middleware

app = FastAPI()

# 미들웨어 등록
app.add_middleware(example_middleware)
>>>>>>> f4aedab (240131 feat: middleware dir changed)
