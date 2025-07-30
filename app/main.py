from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import json
from contextlib import asynccontextmanager

from app.config import config
from app.middleware import LoggingMiddleware, RequestIDMiddleware
from app.forwarder import forwarder


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events cho FastAPI app"""
    # Startup
    logger.info("Forward API Gateway starting up...")
    logger.info(f"Loaded {len(config.routes)} routes from configuration")
    
    yield
    
    # Shutdown
    logger.info("Forward API Gateway shutting down...")
    await forwarder.close()


# Tạo FastAPI app
app = FastAPI(
    title="Forward API Gateway",
    description="Hệ thống trung gian forward request từ hệ thống A sang hệ thống B",
    version="1.0.0",
    lifespan=lifespan
)

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thêm custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Forward API Gateway",
        "version": "1.0.0",
        "available_routes": list(config.routes.keys())
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "forward-api-gateway"}


@app.get("/routes")
async def get_routes():
    """Lấy danh sách các route có sẵn"""
    routes_info = {}
    for route_name, route_config in config.routes.items():
        routes_info[route_name] = {
            "path": route_config.path,
            "target_url": route_config.target_url,
            "timeout": route_config.timeout
        }
    return routes_info


# Tạo dynamic route cho wildcard path
@app.api_route("/forward/{route_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def forward_route(route_name: str, path: str, request: Request):
    """Forward request với route_name và path riêng biệt"""
    
    logger.info(f"Received forward request for route: {route_name}, path: {path}")
    
    try:
        # Forward request
        response = await forwarder.forward_request(route_name, request, path)
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except HTTPException as e:
        logger.error(f"HTTP error in forward request: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in forward request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.server.host,
        port=config.server.port,
        log_level=config.server.log_level.lower(),
        reload=True
    ) 