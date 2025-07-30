import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from loguru import logger

# Import logger sau khi đã setup
from app.logger import logger as app_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware để log tất cả request và response"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Tạo request ID
        request_id = str(uuid.uuid4())
        
        # Log request
        start_time = time.time()
        
        app_logger.info(f"[{request_id}] Request started: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Log response
        end_time = time.time()
        duration = end_time - start_time
        
        app_logger.info(f"[{request_id}] Response status: {response.status_code}")
        app_logger.info(f"[{request_id}] Request completed in {duration:.3f}s")
        
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware để thêm request ID vào header"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Tạo request ID
        request_id = str(uuid.uuid4())
        
        # Thêm request ID vào request headers
        request.headers.__dict__["_list"].append((b"x-request-id", request_id.encode()))
        
        # Process request
        response = await call_next(request)
        
        # Thêm request ID vào response headers
        response.headers["x-request-id"] = request_id
        
        return response 