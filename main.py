from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from roblox_api import get_user_id_from_username, get_user_details

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