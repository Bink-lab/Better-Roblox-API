# Roblox User Info API

This project is a FastAPI-based application that allows users to fetch information about Roblox users using either their `userid` or `username`. The API also includes support for fetching the user's avatar thumbnail.

## Features

- Fetch basic user information (ID, name, display name, description, ban status).
- Fetch user information using either `userid` or `username`.
- Fetch the user's avatar thumbnail URL.

## Endpoints

### `/account/info`

**Method:** `GET`

**Query Parameters:**
- `userid` (optional): The Roblox user ID.
- `username` (optional): The Roblox username.

**Note:** Either `userid` or `username` must be provided.

**Example Requests:**
- Fetch by `userid`: `http://127.0.0.1:8000/account/info?userid=724054979`
- Fetch by `username`: `http://127.0.0.1:8000/account/info?username=Nexoyxyz`

**Example Response:**
```json
{
  "id": 3407,
  "name": "bananaboy",
  "displayName": "Bananaboy",
  "description": "Sup I'm bananaboy not “bananaboy123” Or “bananaboy6362” any of those I'm bananaboy with no numbers in it so im the original bananaboy",
  "isBanned": false,
  "thumbnailUrl": "https://tr.rbxcdn.com/30DAY-Avatar-FF4691BD3BF0CD0B98A4923029C73C29-Png/720/720/Avatar/Png/noFilter"
}
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Bink-lab/Better-Roblox-API
   cd Better-Roblox-API
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API at `http://127.0.0.1:8000`.

## Notes

- Ensure you have an active internet connection to interact with the Roblox APIs.
- If you encounter any issues, check the console logs for error details.