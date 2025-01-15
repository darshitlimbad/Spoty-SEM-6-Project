<?php
    // Start the session
    if(session_status() == PHP_SESSION_NONE) {
        session_start();
    }
    
    if(!isset($_SESSION['user_id'])){
        header("location: ./auth/discord_oauth2.php");
    }else{
        header("location: /");
    }
?>