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

async def get_user_presence(userid: int):
    try:
        presence_url = "https://presence.roblox.com/v1/presence/users"
        payload = {"userIds": [userid]}
        presence_response = requests.post(presence_url, json=payload)
        presence_response.raise_for_status()
        presence_data = presence_response.json()

        if presence_data and presence_data["userPresences"]:
            return presence_data["userPresences"][0]["userPresenceType"]
        else:
            return 0  # Assume offline if no presence data is found
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user presence: {str(e)}")

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

        # Fetch presence
        presence = await get_user_presence(userid)

        user_info = {
            "id": profile_data.get("id"),
            "name": profile_data.get("name"),
            "displayName": profile_data.get("displayName"),
            "description": profile_data.get("description"),
            "isBanned": profile_data.get("isBanned"),
            "thumbnailUrl": thumbnail_image_url,
            "presence": presence
        }

        return user_info
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user details: {str(e)}")
