# Roblox User Info API

This project is a FastAPI-based application that allows users to fetch information about Roblox users using either their `userid` or `username`. The API also includes support for fetching the user's avatar thumbnail.

## Features

- Fetch basic user information (ID, name, display name, description, ban status).
- Fetch user information using either `userid` or `username`.
- Fetch the user's avatar thumbnail URL.
- Track user presence status (online, offline, in-game, etc.).
- Retrieve username history (past usernames).
- Check if the user's inventory is visible.
- Get the user's friends count.
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
  "id": 3615513,
  "errors": [],
  "name": "Wateriscool",
  "displayName": "Wateriscool",
  "description": "",
  "isBanned": false,
  "thumbnailUrl": "https://tr.rbxcdn.com/30DAY-Avatar-6008F228B50EB6A4CF48003544DEA953-Png/720/720/Avatar/Png/noFilter",
  "presence": 0,
  "usernameHistory": [],
  "canView": true,
  "friendsCount": 0
}
```

## Examples

### Example 1: Fetch user information by ID

```bash
curl "http://127.0.0.1:8000/account/info?userid=1"
```

Response:
```json
{
  "id": 1,
  "errors": [],
  "name": "Roblox",
  "displayName": "Roblox",
  "description": "The official Roblox account.",
  "isBanned": false,
  "thumbnailUrl": "https://tr.rbxcdn.com/30DAY-Avatar-E2DF600AE656711D002ED89ABA68B5C3-Png/720/720/Avatar/Png/noFilter",
  "presence": 0,
  "usernameHistory": [],
  "canView": true,
  "friendsCount": 0
}
```

### Example 2: Fetch user information by username

```bash
curl "http://127.0.0.1:8000/account/info?username=Builderman"
```

Response:
```json
{
  "id": 156,
  "errors": [],
  "name": "Builderman",
  "displayName": "Builderman",
  "description": "CEO of Roblox",
  "isBanned": false,
  "thumbnailUrl": "https://tr.rbxcdn.com/30DAY-Avatar-03710290011AF04651F85A649C0D1B6D-Png/720/720/Avatar/Png/noFilter",
  "presence": 0,
  "usernameHistory": [],
  "canView": true,
  "friendsCount": 91
}
```

### Example 3: Handle a non-existent user

```bash
curl "http://127.0.0.1:8000/account/info?username=ThisUserDoesntExist123456789"
```

Response:
```json
{
  "detail": "User not found"
}
```

### Example 4: Python Usage Example

```python
import requests

# Get user by ID
response = requests.get("http://127.0.0.1:8000/account/info?userid=1")
print(f"Status Code: {response.status_code}")
print(f"User Data: {response.json()}")

# Get user by username
response = requests.get("http://127.0.0.1:8000/account/info?username=Builderman")
print(f"Status Code: {response.status_code}")
print(f"User Data: {response.json()}")
```

### Example 5: JavaScript Usage Example

```javascript
// Using Fetch API
fetch('http://127.0.0.1:8000/account/info?userid=1')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Using async/await
async function fetchUserData(username) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/account/info?username=${username}`);
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

fetchUserData('Builderman');
```

### Response Fields

| Field | Description |
|-------|-------------|
| `id` | The Roblox user ID |
| `name` | The user's current username |
| `displayName` | The user's display name |
| `description` | The user's profile description/bio |
| `isBanned` | Boolean indicating if the user is banned |
| `thumbnailUrl` | URL to the user's avatar thumbnail |
| `presence` | User's online status (see Presence Values below) |
| `usernameHistory` | Array of previous usernames |
| `canView` | Boolean indicating if the user's inventory is visible |
| `friendsCount` | Number of friends the user has |
| `errors` | Array of non-critical errors that occurred during the request |

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
- Alternatively, you can create an issue on the [GitHub repository](https://github.com/Bink-lab/Better-Roblox-API/issues) for assistance.