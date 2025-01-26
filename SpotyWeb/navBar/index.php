<?php
    require_once __DIR__.'/../PHP/admin/utils.php';

    if(session_status() == PHP_SESSION_NONE) {
        session_start();
    }

    if(!isset($_SESSION['user_id']) & isset($_COOKIE['refresh_token'])) {
        header('Location: /PHP/index.php');
    }
?>

<header>
    <nav class="navbar">
        <div class="navbar-logo">
            <a href="/">Spoty</a>
        </div>
        <ul class="navbar-links">
        <li><a href="/" class="nav-link">Home</a></li>
        <li><a href="/#features" class="nav-link">Features</a></li>
            <li><a href="/commands" class="nav-link">Commands</a></li>
        <li><a href="/subscription" class="nav-link">Subscription</a></li>

        <?php 
            if(isset($_SESSION['user_id'])) {
                echo "<li><a href='/profile' class='nav-link profile'>profile</a></li>";
                
                if(isAdmin($_SESSION['user_id'])) {
                    echo "<li><a href='/admin' class='nav-link admin'>Admin</a></li>";
                }
                
                echo "<li><a href='/logout' class='nav-link logout'>Log Out</a></li>";

            }else{
                echo "<li><a href='/PHP/index.php' class='nav-link login'>Sign-In</a></li>";
            }
        ?>
        
        </ul>
        <div class="navbar-toggle">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
        </div>
    </nav>
</header>