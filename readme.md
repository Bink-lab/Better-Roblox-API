# Roblox User Info API

This project is a FastAPI-based application that allows users to fetch information about Roblox users using either their `userid` or `username`.

## Features

- Fetch user information using either `userid` or `username`.
- Fetch the user's avatar thumbnail URL.
- Track user presence status (online, offline, in-game, etc.).
- Retrieve username history (past usernames).
- Error handling for API requests.

## Endpoints

### `/account/info`

**Method:** `GET`

**Query Parameters:**
- `userid` (optional): The Roblox user ID.
- `username` (optional): The Roblox username.

**Note:** Either `userid` or `username` must be provided.

**Example Requests:**
- Fetch by `userid`: `http://127.0.0.1:8000/account/info?userid=3407`
- Fetch by `username`: `http://127.0.0.1:8000/account/info?username=bananaboy`

**Example Response:**
```json
{
{
  "id": 3407,
  "errors": [],
  "name": "bananaboy",
  "displayName": "Bananaboy",
  "description": "Sup I'm bananaboy not “bananaboy123”\nOr “bananaboy6362” any of those I'm bananaboy with no numbers in it so im the original bananaboy",
  "isBanned": false,
  "thumbnailUrl": "https://tr.rbxcdn.com/30DAY-Avatar-FF4691BD3BF0CD0B98A4923029C73C29-Png/720/720/Avatar/Png/noFilter",
  "presence": 0,
  "followerCount": 246,
  "friendsCount": 106,
  "usernameHistory": []
}
}
```

### Presence Values

The `presence` field in the response indicates the user's current online status:
- `0`: Offline
- `1`: Online
- `2`: In-game
- `3`: In Studio
- `4`: In-game (Playing Studio)

### Error Handling

The API includes built-in error handling for various scenarios:
- If a user is not found, a 404 error is returned
- If there's an issue with the Roblox API, a 500 error is returned
- Non-critical errors (like failing to fetch thumbnail or presence) are included in the `errors` array in the response

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Bink-lab/Better-Roblox-API
   cd Better-Roblox-API
   ```

- Or, if you would rather get access to the latest features, use the [Unreleased](https://github.com/Bink-lab/Better-Roblox-API/tree/Unreleased) branch.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the API at `http://127.0.0.1:8000`.

## Notes

- Ensure you have an active internet connection to interact with the Roblox APIs.
- If you encounter any issues, check the console logs for error details.
- Alternatively, you can create an issue on the [GitHub repository](https://github.com/Bink-lab/Better-Roblox-API/issues) for assistance.