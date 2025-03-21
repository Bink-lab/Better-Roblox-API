from fastapi import HTTPException
from proxy_manager import get, post

async def get_user_id_from_username(username: str):
    try:
        url = "https://users.roblox.com/v1/usernames/users"
        payload = {"usernames": [username], "excludeBannedUsers": True}
        response = post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if data["data"]:
            return data["data"][0]["id"]
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user ID from username: {str(e)}")

async def get_user_presence(userid: int):
    try:
        presence_url = "https://presence.roblox.com/v1/presence/users"
        payload = {"userIds": [userid]}
        presence_response = post(presence_url, json=payload)
        presence_response.raise_for_status()
        presence_data = presence_response.json()

        if presence_data and presence_data["userPresences"]:
            return presence_data["userPresences"][0]["userPresenceType"]
        else:
            return 0  # Assume offline if no presence data is found
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user presence: {str(e)}")

async def get_username_history(userid: int, limit: int = 10):
    try:
        history_url = f"https://users.roblox.com/v1/users/{userid}/username-history?limit={limit}"
        history_response = get(history_url)
        history_response.raise_for_status()
        history_data = history_response.json()

        if history_data and "data" in history_data:
            return [entry["name"] for entry in history_data["data"]]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch username history: {str(e)}")

async def get_follower_count(userid: int):
    try:
        followers_url = f"https://friends.roblox.com/v1/users/{userid}/followers/count"
        followers_response = get(followers_url)
        followers_response.raise_for_status()
        followers_data = followers_response.json()
        if "count" in followers_data:
            return followers_data["count"]
        else:
            return 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch follower count: {str(e)}")
    

async def get_friends_count(userid: int):
    try:
        friends_count_url = f"https://friends.roblox.com/v1/users/{userid}/friends/count"
        friends_count_response = get(friends_count_url)
        friends_count_response.raise_for_status()
        friends_count_data = friends_count_response.json()

        if "count" in friends_count_data:
            return friends_count_data["count"]
        else:
            return 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch friends count: {str(e)}")

async def get_user_games(userid: int, limit: int = 10):
    try:
        games_url = f"https://games.roblox.com/v2/users/{userid}/games?accessFilter=2&limit={limit}&sortOrder=Asc"
        games_response = get(games_url)
        games_response.raise_for_status()
        games_data = games_response.json()

        if "data" in games_data:
            return games_data["data"]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user games: {str(e)}")

async def get_user_following_count(userid: int):
    try:
        following_url = f"https://friends.roblox.com/v1/users/{userid}/followings/count"
        following_response = get(following_url)
        following_response.raise_for_status()
        following_data = following_response.json()

        if "count" in following_data:
            return following_data["count"]
        else:
            return 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch following count: {str(e)}")

async def get_user_details(userid: int):
    user_info = {
        "id": userid,
        "errors": []
    }
    
    # Fetch basic profile data - this is essential
    try:
        profile_url = f"https://users.roblox.com/v1/users/{userid}"
        profile_response = get(profile_url)
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        # Add core profile data
        user_info.update({
            "name": profile_data.get("name"),
            "displayName": profile_data.get("displayName"),
            "description": profile_data.get("description"),
            "isBanned": profile_data.get("isBanned")
        })
    except Exception as e:
        # Profile data is essential, so we still raise an exception
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profile: {str(e)}")

    # Fetch thumbnail URL - non-essential
    try:
        thumbnail_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=720x720&format=Png&isCircular=false"
        thumbnail_response = get(thumbnail_url)
        thumbnail_response.raise_for_status()
        thumbnail_data = thumbnail_response.json()

        thumbnail_image_url = None
        if thumbnail_data and thumbnail_data["data"]:
            thumbnail_image_url = thumbnail_data["data"][0]["imageUrl"]
        
        user_info["thumbnailUrl"] = thumbnail_image_url
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch thumbnail: {str(e)}")
        user_info["thumbnailUrl"] = None

    # Fetch presence - non-essential
    try:
        presence = await get_user_presence(userid)
        user_info["presence"] = presence
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch presence: {str(e)}")
        user_info["presence"] = 0  # Default to offline

    # Fetch follower count - non-essential
    try:
        follower_count = await get_follower_count(userid)
        user_info["followerCount"] = follower_count
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch follower count: {str(e)}")
        user_info["followerCount"] = 0

    # Fetch following count - non-essential
    try:
        following_count = await get_user_following_count(userid)
        user_info["followingCount"] = following_count
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch following count: {str(e)}")
        user_info["followingCount"] = 0

    # Fetch friends count - non-essential
    try:
        friends_count = await get_friends_count(userid)
        user_info["friendsCount"] = friends_count
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch friends count: {str(e)}")
        user_info["friendsCount"] = 0

    # Fetch username history - non-essential
    try:
        username_history = await get_username_history(userid)
        user_info["usernameHistory"] = username_history
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch username history: {str(e)}")
        user_info["usernameHistory"] = []
    
    # Fetch user games - non-essential
    try:
        user_games = await get_user_games(userid)
        user_info["games"] = user_games
    except Exception as e:
        user_info["errors"].append(f"Failed to fetch user games: {str(e)}")
        user_info["games"] = []


    return user_info
