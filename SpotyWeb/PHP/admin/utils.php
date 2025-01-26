<?php
    // Include the database initialization file
    require_once __DIR__.'/../DB/init_database.php';

    $config_file = __DIR__."/config.json";
    if(!file_exists($config_file)){
        die("Config file missing!");
    }
    
    $config = json_decode(file_get_contents($config_file), true);
    if(json_last_error() !== JSON_ERROR_NONE){
        die("Error: Invalid JSON in config file.");
    }

    if(!is_array($config['admin_ids'])){
        die("Error: Admin ids must be an array.");
    }

    if(!isset($config['admin_ids'])){
        die("Error: Admin ids array is empty.");
    }

    //  Admins ID that can view the admin page
    $adminIds = $config['admin_ids']; 


    // Verify if user ID is an admin or not.
    function isAdmin($userId){
        global $adminIds;

        return in_array($userId, $adminIds);
    }

    // Function to check if user exists
    function UserExists($userId){
        global $PDO;

        $sql = "SELECT * FROM users WHERE id = ?";
        $stmt = $PDO->prepare($sql);
        $stmt->execute([$userId]);

        $result = $stmt->fetch(PDO::FETCH_ASSOC);

        return !empty($result);
    }

    // Function that deletes a user
    function deleteUser($userId){
        global $PDO;

        if(isAdmin($userId))
            return false;
        
        $sql = "DELETE FROM users WHERE id = ?";

        try{

            $stmt = $PDO->prepare($sql);
            $stmt->execute([$userId]);

            // Check how many rows has been affected in sql, for this we will check if its > 0 
            return $stmt->rowCount() > 0;

        }catch(PDOException $e){
            return false;
        }
    }


?>