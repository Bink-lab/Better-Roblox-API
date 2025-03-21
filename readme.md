# Roblox User Info API

This project is a FastAPI-based application that allows users to fetch information about Roblox users using either their `userid` or `username`.

## Features

- Fetch user information using either `userid` or `username`.
- Fetch the user's avatar thumbnail URL.
- Track user presence status (online, offline, in-game, etc.).
- Retrieve username history (past usernames).
- Error handling for API requests.
- Access to user profile description.
- Display name retrieval (separate from username).
- Ban status checking.
- Follower count statistics.
- Friends count statistics.
- Optional proxy support for distributing API requests.
- Support for HTTP, HTTPS, and SOCKS proxies.
- IP-based rate limiting to prevent abuse.

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
  "id": 3407,
  "errors": [],
  "name": "bananaboy",
  "displayName": "Bananaboy",
  "description": "Sup I'm bananaboy not “bananaboy123”\nOr “bananaboy6362” any of those I'm bananaboy with no numbers in it so im the original bananaboy",
  "isBanned": false,
  "thumbnailUrl": "https://tr.rbxcdn.com/30DAY-Avatar-FF4691BD3BF0CD0B98A4923029C73C29-Png/720/720/Avatar/Png/noFilter",
  "presence": 0,
  "followerCount": 247,
  "followingCount": 56,
  "friendsCount": 106,
  "usernameHistory": [],
  "games": [
    {
      "id": 6892035272,
      "name": "Drivin The Systems",
      "description": null,
      "creator": {
        "id": 3407,
        "type": "User"
      },
      "rootPlace": {
        "id": 137677597076446,
        "type": "Place"
      },
      "created": "2024-12-08T02:39:19.647Z",
      "updated": "2024-12-08T18:45:12.933Z",
      "placeVisits": 6
    }
  ]
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

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application (optional):

   - **Configuration File:**
     - Create a `settings.config` file based on the provided example.
     - Edit the `settings.config` file to match your desired configuration.
       ```ini
       [ProxySettings]
       use_proxies = false
       proxy_file = proxies.txt

       [ApiSettings]
       rate_limit = 60
       ```
     - Set `use_proxies` to `true` to enable proxy usage.
   - **Proxy List:**
     - Create a `proxies.txt` file (or any name specified in `settings.config`)
     - Add your proxies, one per line, following the format in `proxies.txt.sample`.
       ```
       http://username:password@proxy.example.com:8080
       https://proxy2.example.com:8080
       socks5://username:password@socks-proxy.example.com:1080
       socks4://socks-proxy.example.com:1080
       ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the API at `http://127.0.0.1:8000`.

## Proxy Configuration

This API supports the use of proxies to distribute requests and avoid rate limits. To use proxies:

1. Create a `settings.config` file as shown above, setting `use_proxies = true`
2. Add proxy URLs to `proxies.txt` (one URL per line) in the format:
   ```
   http://username:password@proxy.example.com:8080
   https://proxy2.example.com:8080
   socks5://username:password@socks-proxy.example.com:1080
   socks4://socks-proxy.example.com:1080
   ```
   
   Note: If you don't specify a protocol, HTTP will be used by default.

3. You can also set proxies via environment variable:
   ```bash
   export ROBLOX_API_PROXIES="http://proxy1.com:8080,socks5://proxy2.com:1080"
   ```

4. Advanced proxy settings in `settings.config`:
   ```ini
   [ProxySettings]
   use_proxies = true
   proxy_file = proxies.txt
   direct_fallback = true  # Fall back to direct connection if all proxies fail
   max_failures = 3        # Number of failures before temporarily blacklisting a proxy
   blacklist_time = 300    # Time in seconds to blacklist a failing proxy (5 minutes)
   ```

The proxy system is designed with smart fallback:
- If a proxy fails, the system will try another one
- Repeatedly failing proxies are temporarily blacklisted
- If all proxies are unavailable and `direct_fallback` is enabled, the API will use a direct connection

**Note:** The proxy feature is designed to distribute requests responsibly. Even with proxies enabled, please use this API responsibly to avoid excessive requests to Roblox services.

## Rate Limiting

The API includes IP-based rate limiting to prevent abuse:

- Each IP address is limited to a configurable number of requests per minute
- When the limit is reached, requests will receive a 429 status code
- Rate limit information is included in response headers:
  - `X-RateLimit-Limit`: Maximum allowed requests per minute
  - `X-RateLimit-Remaining`: Remaining requests for the current window
  - `X-RateLimit-Reset`: Time in seconds until the rate limit resets

To configure rate limiting, add the following to your `settings.config`:

```ini
[ApiSettings]
enable_rate_limit = true
rate_limit = 60  # Requests per minute per IP address
```

## Notes

- Ensure you have an active internet connection to interact with the Roblox APIs.
- If you encounter any issues, check the console logs for error details.
- Alternatively, you can create an issue on the [GitHub repository](https://github.com/Bink-lab/Better-Roblox-API/issues) for assistance.