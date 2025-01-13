<?php
    if(!isset($_GET['pass']) OR $_GET['pass'] != "gharbhegutha") {
        echo "Invalid Password";
        header('Location: /');
    }else{
        // add subscribe logic here
        header('Location: https://youtube.com/shorts/QexSldF9jOY?si=v-223JlvpeRBVh5s');
    }
?>