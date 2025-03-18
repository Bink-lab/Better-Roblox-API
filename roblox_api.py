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

async def get_username_history(userid: int, limit: int = 10):
    try:
        history_url = f"https://users.roblox.com/v1/users/{userid}/username-history?limit={limit}"
        history_response = requests.get(history_url)
        history_response.raise_for_status()
        history_data = history_response.json()

        if history_data and "data" in history_data:
            return [entry["name"] for entry in history_data["data"]]
        else:
            return []
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch username history: {str(e)}")

async def get_user_friends_count(userid: int):
    try:
        friends_url = f"https://friends.roblox.com/v1/users/{userid}/friends/count"
        friends_response = requests.get(friends_url)
        friends_response.raise_for_status()
        friends_data = friends_response.json()
        return friends_data.get("count", 0)  # Return the count value from the response
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user friends count: {str(e)}")

async def can_view_inventory(userid: int):
    try:
        inventory_url = f"https://inventory.roblox.com/v1/users/{userid}/can-view-inventory"
        inventory_response = requests.get(inventory_url)
        inventory_response.raise_for_status()
        inventory_data = inventory_response.json()
        return inventory_data.get("canView", False)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user inventory visibility: {str(e)}")


async def get_user_details(userid: int):
    user_info = {
        "id": userid,
        "errors": []
    }
    
    # Fetch basic profile data - this is essential
    try:
        profile_url = f"https://users.roblox.com/v1/users/{userid}"
        profile_response = requests.get(profile_url)
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        # Add core profile data
        user_info.update({
            "name": profile_data.get("name"),
            "displayName": profile_data.get("displayName"),
            "description": profile_data.get("description"),
            "isBanned": profile_data.get("isBanned")
        })
    except requests.exceptions.RequestException as e:
        # Profile data is essential, so we still raise an exception
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profile: {str(e)}")

    # Fetch thumbnail URL - non-essential
    try:
        thumbnail_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=720x720&format=Png&isCircular=false"
        thumbnail_response = requests.get(thumbnail_url)
        thumbnail_response.raise_for_status()
        thumbnail_data = thumbnail_response.json()

        thumbnail_image_url = None
        if (thumbnail_data and thumbnail_data["data"]):
            thumbnail_image_url = thumbnail_data["data"][0]["imageUrl"]
        
        user_info["thumbnailUrl"] = thumbnail_image_url
    except requests.exceptions.RequestException as e:
        user_info["errors"].append(f"Failed to fetch thumbnail: {str(e)}")
        user_info["thumbnailUrl"] = None

    # Fetch presence - non-essential
    try:
        presence = await get_user_presence(userid)
        user_info["presence"] = presence
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch presence: {str(e)}")
        user_info["presence"] = 0  # Default to offline

    # Fetch username history - non-essential
    try:
        username_history = await get_username_history(userid)
        user_info["usernameHistory"] = username_history
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch username history: {str(e)}")
        user_info["usernameHistory"] = []

    # Fetch inventory visibility - non-essential
    try:
        inventory_visible = await can_view_inventory(userid)
        user_info["canView"] = inventory_visible
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch inventory visibility: {str(e)}")
        user_info["canView"] = False  # Default to not being able to view inventory

    # Fetch friends count - non-essential
    try:
        friends_count = await get_user_friends_count(userid)
        user_info["friendsCount"] = friends_count
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch friends count: {str(e)}")
        user_info["friendsCount"] = 0  # Set a default value when there's an error
    return user_info