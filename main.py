from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from roblox_api import get_user_id_from_username, get_user_details
from proxy_manager import proxy_manager
from rate_limiter import rate_limiter
import os
import configparser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Load environment proxies if available
    env_proxies = os.environ.get("ROBLOX_API_PROXIES", "")
    if env_proxies:
        proxy_list = [p.strip() for p in env_proxies.split(",") if p.strip()]
        proxy_manager.add_proxies(proxy_list)
        if proxy_list:
            logger.info(f"Loaded {len(proxy_list)} proxies from environment variables")
    
    # Print proxy status
    if proxy_manager.enabled:
        logger.info(f"Proxy support is enabled with {len(proxy_manager.proxies)} proxies")
        logger.info(f"Proxy direct fallback: {'Enabled' if proxy_manager.direct_fallback else 'Disabled'}")
    else:
        logger.info("Proxy support is disabled")
        
    # Print rate limit info
    if rate_limiter.enabled:
        logger.info(f"Rate limiting is enabled: {rate_limiter.rate_limit} requests per minute per IP")
    else:
        logger.info("Rate limiting is disabled")

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Get client IP address
    client_ip = request.client.host
    
    # Skip rate limiting for certain paths if needed
    if request.url.path == "/docs" or request.url.path == "/openapi.json":
        return await call_next(request)
    
    # Check rate limit
    if rate_limiter.is_rate_limited(client_ip):
        reset_time = rate_limiter.get_reset_time(client_ip)
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests. Please try again later.",
                "reset_in_seconds": reset_time
            }
        )
    
    # Process the request
    response = await call_next(request)
    
    # Add rate limit headers
    if isinstance(response, Response):
        remaining = rate_limiter.get_remaining_requests(client_ip)
        reset_time = rate_limiter.get_reset_time(client_ip)
        
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        if reset_time:
            response.headers["X-RateLimit-Reset"] = str(int(reset_time))
    
    return response

@app.get("/account/info")
async def get_account_info(userid: int = None, username: str = None):
    if not userid and not username:
        raise HTTPException(status_code=400, detail="Either userid or username must be provided")

    try:
        if username:
            userid = await get_user_id_from_username(username)

        user_info = await get_user_details(userid)
        return JSONResponse(content=user_info)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")