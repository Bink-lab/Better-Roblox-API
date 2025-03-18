from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from roblox_api import get_user_id_from_username, get_user_details
import uvicorn
import os

app = FastAPI()

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

# Add a root endpoint for health checks
@app.get("/")
async def root():
    return {"message": "Roblox User Info API is running. Use /account/info endpoint."}

# This will be used when the file is run directly
if __name__ == "__main__":
    # Get port from environment variable or use default 10000 (Render's default)
    port = int(os.environ.get("PORT", 10000))
    # Run the app with uvicorn, binding to 0.0.0.0
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
