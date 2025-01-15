<?php
    // Start the session
    if(session_status() == PHP_SESSION_NONE) {
        session_start();
    }

    if(!isset($_SESSION['user_id'])) {
        echo "Please sign in first!";
        header('Location: /PHP/index.php');
    }else if(!isset($_GET['pass']) OR $_GET['pass'] != "gharbhegutha") {
        echo "Invalid Password";
        header('Location: /');
    }else{
        include "DB/init_database.php";
        $stmt = $pdo->prepare("UPDATE users SET premium = 1 WHERE id = ?");
        $stmt->execute([$_SESSION['user_id']]);
        echo "Subscribed Successfully!";
        header('Location: https://youtube.com/shorts/QexSldF9jOY?si=v-223JlvpeRBVh5s');
    }
?>