# app/middleware/example_middleware.py
from fastapi import Request, HTTPException

async def example_middleware(request: Request, call_next):
    # Middleware 전처리 로직
    print("Executing example middleware before request processing.")
    
    # 다음 미들웨어 또는 엔드포인트 호출
    response = await call_next(request)
    
    # Middleware 후처리 로직
    print("Executing example middleware after request processing.")
    
    return response
