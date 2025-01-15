<?php
    if(session_status() == PHP_SESSION_NONE) {
        session_start();
    }

    setcookie('refresh_token', '', time() - 3600, '/');
    session_destroy();
    session_abort();
    header("Location: /");
    exit();
?>