<?php
// Load config
$config = json_decode(file_get_contents(__DIR__ . '/config.json'), true);
if (json_last_error() !== JSON_ERROR_NONE) die("Error: Invalid JSON in config file.");

// Extract OAuth configuration
$clientId = $config['oauth']['clientId'];
$clientSecret = $config['oauth']['clientSecret'];
$redirectUri = $config['oauth']['redirectUri'];

// Database connection
include_once("../DB/init_database.php");

// URLs
$discordAuthUrl = "https://discord.com/api/oauth2/authorize?client_id=$clientId&response_type=code&redirect_uri=" . urlencode($redirectUri) . "&scope=identify+email";
$tokenUrl = 'https://discord.com/api/oauth2/token';
$userApiUrl = 'https://discord.com/api/users/@me';

// Step 0: Check for Refresh Token in Cookies
session_start();
if (isset($_COOKIE['refresh_token'])) {
    // Refresh token exists, try to get new access token
    $refreshToken = $_COOKIE['refresh_token'];
    $ch = curl_init($tokenUrl);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query([
            'client_id' => $clientId,
            'client_secret' => $clientSecret,
            'grant_type' => 'refresh_token',
            'refresh_token' => $refreshToken
        ]),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/x-www-form-urlencoded']
    ]);
    $response = curl_exec($ch);
    curl_close($ch);

    $tokenData = json_decode($response, true);

    // Check if access token is returned
    if (isset($tokenData['access_token'])) {
        // Fetch user info
        $accessToken = $tokenData['access_token'];
        $ch = curl_init($userApiUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ["Authorization: Bearer $accessToken"]);
        $userData = json_decode(curl_exec($ch), true);
        curl_close($ch);

        if (isset($userData['id'])) {
            // Save user and refresh token to DB
            saveUserData($userData, $accessToken, $tokenData['refresh_token'], $tokenData['expires_in']);
            setcookie('refresh_token', $tokenData['refresh_token'], time() + 60*60*24*30, "/"); 
            $_SESSION['user_id'] = $userData['id'];
            $_SESSION['username'] = $userData['username'];
            header("Location: /PHP/index.php");
            exit;
        }
    } else {
        // If an error occurs or refresh token is invalid, delete the cookie
        setcookie('refresh_token', '', time() - 3600, '/'); // Delete the refresh token cookie
        header("Refresh:0");
    }

} else {
    // No refresh token in cookies, initiate OAuth flow

    // Step 1: OAuth Code Flow if no valid refresh token
    if (!isset($_GET['code'])) {
        header("Location: $discordAuthUrl");
        exit;  // Ensure no further code execution
    }

    // Step 2: Exchange Code for Access Token
    $code = $_GET['code'];
    $ch = curl_init($tokenUrl);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query([
            'client_id' => $clientId,
            'client_secret' => $clientSecret,
            'grant_type' => 'authorization_code',
            'code' => $code,
            'redirect_uri' => $redirectUri
        ]),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/x-www-form-urlencoded']
    ]);
    $response = curl_exec($ch);
    curl_close($ch);

    $tokenData = json_decode($response, true);
    if (isset($tokenData['access_token'])) {
        // Fetch user info
        $accessToken = $tokenData['access_token'];
        $ch = curl_init($userApiUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ["Authorization: Bearer $accessToken"]);
        $userData = json_decode(curl_exec($ch), true);
        curl_close($ch);

        if (isset($userData['id'])) {
            // Save user and refresh token to DB
            saveUserData($userData, $accessToken, $tokenData['refresh_token'], $tokenData['expires_in']);
            setcookie('refresh_token', $tokenData['refresh_token'], time() + 60*60*24*30, "/");  // Cookie expires in 30 days

            $_SESSION['user_id'] = $userData['id'];
            $_SESSION['username'] = $userData['username'];
            header("Location: /PHP/index.php");
            exit;
        }
    } else {
        die("Error: Unable to authenticate user.");
    }
}

// Helper function to save user data and refresh token
function saveUserData($userData, $accessToken, $refreshToken, $expires_in) {
    global $pdo;
    try {
        $sql = "INSERT INTO users (id, username, discriminator, avatar, access_token, refresh_token, token_expires_at, last_login)
                VALUES (:id, :username, :discriminator, :avatar, :access_token, :refresh_token, :token_expires_at, :last_login)
                ON DUPLICATE KEY UPDATE
                    username = :username,
                    discriminator = :discriminator,
                    avatar = :avatar,
                    access_token = :access_token,
                    refresh_token = :refresh_token,
                    token_expires_at = :token_expires_at,
                    last_login = :last_login";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([
            ':id' => $userData['id'],
            ':username' => $userData['username'],
            ':discriminator' => $userData['discriminator'],
            ':avatar' => $userData['avatar'] ?? null,
            ':access_token' => $accessToken,
            ':refresh_token' => $refreshToken,
            ':token_expires_at' => date('Y-m-d H:i:s', time() + $expires_in),
            ':last_login' => date('Y-m-d H:i:s')
        ]);
    } catch (PDOException $e) {
        die("Error saving user data: " . $e->getMessage());
    }
}
?>
