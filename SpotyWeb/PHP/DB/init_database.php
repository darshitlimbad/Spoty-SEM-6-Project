<?php
// Path to the config.json file
$configFile = __DIR__ . '/config.json';

if (!file_exists($configFile)) {
    die("Error: Config file not found.");
}

// Read and decode the JSON file
$jsonContent = file_get_contents($configFile);
$config = json_decode($jsonContent, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    die("Error: Invalid JSON in config file.");
}

// Extract database configuration
$dbHost = $config['database']['host'];
$dbUsername = $config['database']['username'];
$dbPassword = $config['database']['password'];
$dbName = $config['database']['dbname'];

try {
    // Connect to MySQL server (without specifying a database)
    $pdo = new PDO("mysql:host=$dbHost", $dbUsername, $dbPassword);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Check if the database exists and create it if not
    $pdo->exec("CREATE DATABASE IF NOT EXISTS $dbName");

    // Switch to the specified database
    $pdo->exec("USE $dbName");

    // Create the "users" table if it doesn't exist
    $tableQuery = "
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(20) PRIMARY KEY,        -- Discord user ID
            username VARCHAR(100),            -- Username
            discriminator VARCHAR(4),         -- Discriminator (e.g., #1234)
            avatar VARCHAR(255),              -- Avatar hash
            access_token TEXT,                -- OAuth2 access token
            refresh_token TEXT,               -- OAuth2 refresh token
            token_expires_at DATETIME,        -- Expiry timestamp for the access token
            last_login DATETIME               -- Timestamp of the last login
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ";
    $pdo->exec($tableQuery);
} catch (PDOException $e) {
    die("Error: " . $e->getMessage()); 
}
?>
