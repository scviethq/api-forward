#!/usr/bin/env python3
"""
Test script cho Forward API Gateway
"""

import asyncio
import httpx
import json
from loguru import logger


async def test_health_check():
    """Test health check endpoint"""
    logger.info("Testing health check...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/health")
        
        if response.status_code == 200:
            logger.success("✅ Health check passed")
            logger.info(f"Response: {response.json()}")
        else:
            logger.error(f"❌ Health check failed: {response.status_code}")


async def test_get_routes():
    """Test get routes endpoint"""
    logger.info("Testing get routes...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/routes")
        
        if response.status_code == 200:
            logger.success("✅ Get routes passed")
            routes = response.json()
            logger.info(f"Available routes: {list(routes.keys())}")
            
            for route_name, route_info in routes.items():
                logger.info(f"  - {route_name}: {route_info['method']} -> {route_info['target_url']}")
        else:
            logger.error(f"❌ Get routes failed: {response.status_code}")


async def test_forward_request():
    """Test forward request"""
    logger.info("Testing forward request...")
    
    # Test data
    test_data = {
        "order_id": "TEST-001",
        "customer_id": "CUST-123",
        "items": [
            {"product_id": "PROD-001", "quantity": 2, "price": 100}
        ]
    }
    
    async with httpx.AsyncClient() as client:
        # Test POST request
        response = await client.post(
            "http://localhost:8000/api/forward/salesorder_create",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"Forward request status: {response.status_code}")
        
        if response.status_code in [200, 201, 404, 502, 504]:
            logger.success("✅ Forward request test completed")
            logger.info(f"Response status: {response.status_code}")
            
            try:
                response_data = response.json()
                logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            except:
                logger.info(f"Response text: {response.text[:200]}...")
        else:
            logger.error(f"❌ Unexpected status code: {response.status_code}")


async def test_forward_with_params():
    """Test forward request with query parameters"""
    logger.info("Testing forward request with query parameters...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/forward/inventory_sync",
            params={"warehouse": "main", "category": "electronics"}
        )
        
        logger.info(f"Forward with params status: {response.status_code}")
        
        if response.status_code in [200, 404, 502, 504]:
            logger.success("✅ Forward with params test completed")
        else:
            logger.error(f"❌ Unexpected status code: {response.status_code}")


async def test_forward_with_path_params():
    """Test forward request with path parameters"""
    logger.info("Testing forward request with path parameters...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/forward/customer_info/123"
        )
        
        logger.info(f"Forward with path params status: {response.status_code}")
        
        if response.status_code in [200, 404, 502, 504]:
            logger.success("✅ Forward with path params test completed")
        else:
            logger.error(f"❌ Unexpected status code: {response.status_code}")


async def test_invalid_route():
    """Test invalid route"""
    logger.info("Testing invalid route...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/forward/invalid_route")
        
        if response.status_code == 404:
            logger.success("✅ Invalid route test passed (404 as expected)")
        else:
            logger.error(f"❌ Invalid route test failed: {response.status_code}")


async def main():
    """Run all tests"""
    logger.info("🚀 Starting Forward API Gateway tests...")
    
    try:
        await test_health_check()
        await asyncio.sleep(1)
        
        await test_get_routes()
        await asyncio.sleep(1)
        
        await test_forward_request()
        await asyncio.sleep(1)
        
        await test_forward_with_params()
        await asyncio.sleep(1)
        
        await test_forward_with_path_params()
        await asyncio.sleep(1)
        
        await test_invalid_route()
        
        logger.success("🎉 All tests completed!")
        
    except httpx.ConnectError:
        logger.error("❌ Cannot connect to server. Make sure the server is running on localhost:8000")
    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main()) 