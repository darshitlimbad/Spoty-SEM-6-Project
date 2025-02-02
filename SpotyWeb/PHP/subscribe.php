<?php
    include "DB/init_database.php";
    if(!$PDO){
        echo "Database Connection Error!";
        die();
    }
    
    // Start the session
    if(session_status() == PHP_SESSION_NONE) {
        session_start();
    }

    if(isset($_GET['action']) AND $_GET['action'] == "issubscribed"){
        if(!isset($_SESSION['user_id'])) {
            echo "0";
            die();
        }

        $stmt = $PDO->prepare("SELECT premium FROM users WHERE id = ?");
        $res= $stmt->execute([$_SESSION['user_id']]);
        if(!$res){
            echo "Error!";
            die();
        }
        echo $stmt->fetch()['premium'];
    }

    if(!isset($_SESSION['user_id'])) {
        echo "Please sign in first!";
        header('Location: /PHP/index.php');
        die();
    }
    
    if(!isset($_GET['pass']) OR $_GET['pass'] != "gharbhegutha") {
        echo "Invalid Password";
        header('Location: /');
        die();
    }

    if(isset($_GET['action']) AND $_GET['action'] == "unsubscribe"){
        $stmt = $PDO->prepare("UPDATE users SET premium = 0 WHERE id = ?");
        $stmt->execute([$_SESSION['user_id']]);
        echo "Unsubscribed Successfully!";
        header('Location: /subscription');
    }
    
    if(isset($_GET['action']) AND $_GET['action'] == "subscribe"){
        $stmt = $PDO->prepare("UPDATE users SET premium = 1 WHERE id = ?");
        $stmt->execute([$_SESSION['user_id']]);
        echo "Subscribed Successfully!";
        header('Location: https://youtube.com/shorts/QexSldF9jOY?si=v-223JlvpeRBVh5s');
    }
?>