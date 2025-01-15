# Spoty Music Companion for Discord - Project Abstraction

## 1. Project Overview

*   **Project Title:** Spoty Music Companion for Discord
*   **Bot Display Name:** Spoty
*   **Primary Goal:** To provide a flexible and enhanced music experience within Discord servers. This is achieved by offering:
    *   **Comprehensive Search:** Supporting a wide range of music, including less popular or region-specific songs.
    *   **Flexible Input:** Allowing users to play music via song queries, direct URLs, and entire playlist URLs.
    *   **Seamless Queue Management:** Ensuring easy addition of multiple songs via playlist support.

## 2. "spoty" (Backend) Abstraction

*   **Core Technologies:** Python 3.8+, `discord.py`, `yt_dlp`, `PyNaCl`, `mysql-connector-python`.
*   **Functionality:**
    *   **Discord Interaction:**
        *   Uses `discord.py` library for all Discord interactions.
        *   Implements both prefix-based and slash commands.
        *   Manages voice channel connections (join, disconnect).
        *   Utilizes `on_voice_state_update` to auto-disconnect if the bot is the only member.
        *   Uses `is_user_authorized_to_control` for command authorization.
        *   Uses `asyncio.loop.run_in_executor` for non-blocking operations.
    *   **Music Playback:**
        *   Uses `discord.FFmpegPCMAudio` and `PCMVolumeTransformer` for audio playback.
        *   Supports playing from queries, URLs, and Playlists.
        *   Has the functionality to repeat song using `song_repeat` variable.
        *   Has auto-play functionality.
    *   **Queue Management:**
        *   Implements a custom `Queue` class using a Python list.
        *   Provides methods for `put`, `get`, `merge`, `clear`, `shuffle_index`, `is_empty`, and `qsize`.
    *   **Error Handling:** Manages command and playback errors gracefully using embeds and logging.
    *   **Configuration:** Reads configuration from `config.json`.
*   **Data Sources:**
    *   Uses `yt_dlp` to extract audio from various websites, primarily YouTube for now.
    *   **`search_song`:** Searches YouTube for a song based on a query.
    *   **`search_by_query`:** Searches YouTube for a song based on a query or URL.
    *   **`fetch_playlist`:** Fetches songs from a YouTube playlist. It uses the best audio format and ignores unavailable songs.
    *   **`format_queue`:** Formats the song queue into a string for display in a Discord embed.
*   **Database Integration:**
    *   Uses `mysql-connector-python` to connect to a MySQL database.
    *   **Connection Management:**
        *   Initializes a connection based on config file.
        *   Creates a database and a `users` table if they don't exist.
        *   Manages connection pooling and closing.
    *   **User Data:** Stores user data in the `users` table which includes `id`, `username`, `discriminator`, `avatar`, `access_token`, `refresh_token`, `token_expires_at`, `last_login`, and `premium` status.
    *   **User Operations:**
        *   Provides functions to check `is_user_registered` and `is_user_premium`.

## 3. "spotyWeb" (Frontend) Abstraction

*   **Core Technologies:** HTML, CSS, JavaScript, PHP
*   **Functionality:**
    *   **Key Features:**
        *   **Login Page:** Presents a clean login page with a background video and a "Sign in with Discord" button.
        *   **User Authentication:** Handles user authentication via Discord's OAuth2 flow.
        *   **(Future) Feature Showcase:** A section to showcase the music bot's features will be added later.
         *   **(Future) User Profile Page:** User will be redirected to the user profile page from `PHP/index.php` after a successful login.
    *   **Discord Login:**
        *   The login process is initiated by clicking the "Sign in with Discord" button.
        *   It redirects users to Discord's authorization page.
        *   After authorization, Discord redirects the user back to `discord_oauth2.php`.
    *   **User Interaction:** Currently, users only interact with the login button. Further features will be added later.
    *   **Backend Communication:** The `discord_oauth2.php` script directly interacts with the MySQL database and doesn't communicate with the "spoty" backend (Python bot) directly.
*   **User Authentication:**
    *   **OAuth2 Flow:** Implements the full OAuth2 flow (authorization code grant type) for Discord authentication:
        *   **Authorization Request:** Redirects users to Discord's authorization endpoint (`https://discord.com/api/oauth2/authorize`) with necessary parameters.
        *   **Token Exchange:** Exchanges the authorization code for an access token and refresh token at Discord's token endpoint (`https://discord.com/api/oauth2/token`).
        *   **User Data Retrieval:** Uses the access token to fetch user information from Discord's user endpoint (`https://discord.com/api/users/@me`).
        *   **Token Refresh:** Implements refresh token functionality by storing the refresh token in a cookie, using it to obtain new tokens when the access token expires. If no refresh token is found, the OAuth flow is reinitiated.
    *   **Database Storage:** Stores user info, access token, and refresh token in the `users` table in MySQL database.
    *   **Session Management:** Uses PHP sessions to store `user_id` and `username` after successful login.
    *   **Cookie management:** Sets the refresh token in a cookie named `refresh_token` with a 30-day expiration.
*   **Presentation:**
    *   Uses a visually appealing layout with a background video using `index.css`.
    *   A large, central button for easy login.
*   **Database Initialization:**
    *   **`init_database.php`:** Creates a PDO connection to the database using configuration from `PHP/DB/config.json`.
        *   Creates the database and the `users` table if they don't exist.
        *   Sets error mode to `PDO::ERRMODE_EXCEPTION`.

## 4. Database Details

*   **Database System:** MySQL
*   **Database Schema:**
    *   **`users` Table:**
        *   `id` (VARCHAR(20), PRIMARY KEY): Discord user ID.
        *   `username` (VARCHAR(100)): Discord username.
        *   `discriminator` (VARCHAR(4)): Discord discriminator (e.g., #1234).
        *   `avatar` (VARCHAR(255)): Discord avatar hash.
        *   `access_token` (TEXT): OAuth2 access token.
        *   `refresh_token` (TEXT): OAuth2 refresh token.
        *   `token_expires_at` (DATETIME): Expiry timestamp for the access token.
        *   `last_login` (DATETIME): Timestamp of the last login.
        *    `premium` (TINYINT(1), DEFAULT 0): Premium status.

## 5. Overall Project Flow

1.  **User Discovery:** Users find the "Spoty" bot on Discord.
2.  **Discord Interaction:**
    *   Users use bot commands via Discord to play music.
    *   The bot connects to voice channels, plays audio, and manages queues, using the `yt_dlp` library to fetch audio, `discord.py` library to interact with Discord and a custom queue to manage the song requests.
3.  **Web Login:**
    *   Users navigate to the "spotyWeb" login page.
    *   They click "Sign in with Discord", which redirects them to Discord for authorization.
    *   Upon authorization, users are redirected back to the site where their access and refresh tokens are stored in a cookie and the database.
    *   After Successful login user is redirected to `/PHP/index.php` which will eventually lead to their profile page.
4.  **Database Storage:** User information and tokens are stored in the MySQL database.