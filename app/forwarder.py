import re
from typing import Dict, Any, Optional
import httpx
from fastapi import Request, HTTPException
from loguru import logger
from app.config import config


class RequestForwarder:
    """Class để forward request từ hệ thống A sang hệ thống B"""
    
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def close(self):
        """Đóng HTTP client"""
        await self.client.aclose()

    async def forward_request(
        self, 
        route_name: str, 
        request: Request,
        path: str = None  # Thêm parameter path
    ) -> httpx.Response:
        """Forward request đến hệ thống đích"""
        
        if route_name not in config.routes:
            raise HTTPException(status_code=404, detail=f"Route '{route_name}' not found")
        
        route_config = config.routes[route_name]
        target_url = route_config.target_url.replace("{path:path}", path or '')

        # Lấy headers từ request gốc (loại bỏ một số headers không cần thiết)
        headers = dict(request.headers)
        headers_to_remove = ['host', 'content-length', 'transfer-encoding']
        for header in headers_to_remove:
            headers.pop(header.lower(), None)
        
        # Lấy body từ request
        body = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            body = await request.body()
        
        # Lấy query parameters
        query_params = dict(request.query_params)
        
        logger.info(f"Forwarding request to: {target_url}")
        logger.info(f"Method: {request.method}")
        # logger.info(f"Headers: {headers}")
        logger.info(f"Query params: {query_params}")
        
        try:
            # Thực hiện request đến hệ thống đích
            response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=query_params,
                content=body,
                timeout=route_config.timeout
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            return response
            
        except httpx.TimeoutException:
            logger.error(f"Request timeout to {target_url}")
            raise HTTPException(status_code=504, detail="Gateway timeout")
        except httpx.ConnectError:
            logger.error(f"Connection error to {target_url}")
            raise HTTPException(status_code=502, detail="Bad gateway")
        except Exception as e:
            logger.error(f"Error forwarding request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


# Global forwarder instance
forwarder = RequestForwarder() 