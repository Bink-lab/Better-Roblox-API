import requests
from fastapi import HTTPException

async def get_user_id_from_username(username: str):
    try:
        url = "https://users.roblox.com/v1/usernames/users"
        payload = {"usernames": [username], "excludeBannedUsers": True}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if data["data"]:
            return data["data"][0]["id"]
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user ID from username: {str(e)}")

async def get_user_details(userid: int):
    try:
        profile_url = f"https://users.roblox.com/v1/users/{userid}"
        profile_response = requests.get(profile_url)
        profile_response.raise_for_status()
        profile_data = profile_response.json()

        # Fetch thumbnail URL
        thumbnail_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=720x720&format=Png&isCircular=false"
        thumbnail_response = requests.get(thumbnail_url)
        thumbnail_response.raise_for_status()
        thumbnail_data = thumbnail_response.json()

        thumbnail_image_url = None
        if thumbnail_data and thumbnail_data["data"]:
            thumbnail_image_url = thumbnail_data["data"][0]["imageUrl"]

        user_info = {
            "id": profile_data.get("id"),
            "name": profile_data.get("name"),
            "displayName": profile_data.get("displayName"),
            "description": profile_data.get("description"),
            "isBanned": profile_data.get("isBanned"),
            "thumbnailUrl": thumbnail_image_url
        }

        return user_info
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user details: {str(e)}")
