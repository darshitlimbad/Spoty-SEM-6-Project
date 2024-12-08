<?php
    // Start the session
    session_start();
    if(!isset($_SESSION['user_id'])){
        header("location: ./auth/discord_oauth2.php");
    }
?>