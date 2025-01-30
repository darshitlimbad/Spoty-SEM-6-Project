<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spoty - Music Discord Bot</title>
    <link rel="stylesheet" href="CSS/index.css">
    <link rel="stylesheet" href="CSS/navbar.css">
</head>
<body>
    <?php
        include_once("./navBar/index.php");
    ?>

    <div class="scroll-container">
        <!-- Home Page Section -->
        <section id="home" class="page active">
            <!-- Home Content -->
            <div class="home-content">
                <h1>Spoty: Your Music Companion</h1>
                <p>Elevate your Discord music experience with seamless controls and high-quality audio</p>
                                
                <div class="button-container">

                <?php
                    if(isset($_SESSION['user_id'])) {
                ?>

                        <!-- Add bot in server button -->
                        <a href="https://discord.com/oauth2/authorize?client_id=1270715891402674207" target="_blank">
                            <button class="btn btn-discord">
                                Add bot in server
                                <span class="icon-container">
                                    <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                                        <path d="M13.545 2.907a13.227 13.227 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.19 12.19 0 0 0-3.658 0 8.258 8.258 0 0 0-.412-.833.051.051 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.041.041 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032c.001.014.01.028.021.037a13.276 13.276 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019c.308-.42.582-.863.818-1.329a.05.05 0 0 0-.01-.059.051.051 0 0 0-.018-.011 8.875 8.875 0 0 1-1.248-.595.05.05 0 0 1-.02-.066.051.051 0 0 1 .015-.019c.084-.063.168-.129.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.052.052 0 0 1 .053.007c.08.066.164.132.248.195a.051.051 0 0 1-.004.085 8.254 8.254 0 0 1-1.249.594.05.05 0 0 0-.03.03.052.052 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.235 13.235 0 0 0 4.001-2.02.049.049 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.034.034 0 0 0-.02-.019Zm-8.198 7.307c-.789 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612Zm5.316 0c-.788 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612Z"/>
                                    </svg>
                                </span>
                            </button>
                        </a>

                        <!-- User Profile button -->
                        <button class="btn btn-onlyfans" onclick="window.location.href='/Profile'">
                            <?php  echo "Welcome back, @{$_SESSION['username']}"; ?>
                        </button>
                <?php
                    }else{
                ?>

                    <!-- Discord Login Button -->
                    <button class="btn btn-discord" onclick="window.location.href='/PHP/index.php'">
                        Sign in with Discord
                        <span class="icon-container">
                            <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                                <path d="M13.545 2.907a13.227 13.227 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.19 12.19 0 0 0-3.658 0 8.258 8.258 0 0 0-.412-.833.051.051 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.041.041 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032c.001.014.01.028.021.037a13.276 13.276 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019c.308-.42.582-.863.818-1.329a.05.05 0 0 0-.01-.059.051.051 0 0 0-.018-.011 8.875 8.875 0 0 1-1.248-.595.05.05 0 0 1-.02-.066.051.051 0 0 1 .015-.019c.084-.063.168-.129.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.052.052 0 0 1 .053.007c.08.066.164.132.248.195a.051.051 0 0 1-.004.085 8.254 8.254 0 0 1-1.249.594.05.05 0 0 0-.03.03.052.052 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.235 13.235 0 0 0 4.001-2.02.049.049 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.034.034 0 0 0-.02-.019Zm-8.198 7.307c-.789 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612Zm5.316 0c-.788 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612Z"/>
                            </svg>
                        </span>
                    </button>
                        
                    <!-- OnlyFans Login Button -->
                    <a href="https://youtu.be/dQw4w9WgXcQ?si=QIBHvQybqIw9x97D" target="_blank">
                        <button class="btn btn-onlyfans">
                            <span>Login with LonlyFans</span>
                            <svg class="icon" viewBox="150 80 350 350" xmlns="http://www.w3.org/2000/svg">
                                <style>
                                    .st0{fill:none;}
                                    .st1{fill:#00AEEF;}
                                    .st2{fill:#008CCF;}
                                </style>
                                <rect x="71" y="29.3" class="st0" width="400" height="400"/>
                                <path class="st1" d="M 273 144.3 c -61.1 0 -110.5 54.4 -110.5 121.5 s 49.4 121.5 110.5 121.5 s 110.5 -54.4 110.5 -121.5 S 334.1 144.3 273 144.3 z M 273 302.2 c -18.3 0 -33.2 -16.3 -33.2 -36.5 s 14.8 -36.4 33.2 -36.4 s 33.1 16.3 33.1 36.4 c 0 20.1 -14.8 36.4 -33 36.5 C 273.1 302.2 273 302.2 273 302.2 z"/>
                                <path class="st2" d="M 414.6 249.5 c 33.9 8.1 74 0 74 0 c -11.6 42.2 -48.5 68.6 -101.6 71.8 c -21.1 40.6 -69.2 67 -122.4 66.9 L 304.6 282.4 c 41.2 -108.8 62.3 -116.2 159.9 -116.2 h 67 C 520.3 207.4 481.6 238.7 414.6 249.5 z"/>
                            </svg>
                        </button>
                    </a>
                    
                </div>
                <?php
                    }
                ?>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="page">
             <!-- Removing this background video cause it will take more bandwidth for no reason -->
            <!-- Background Video -->
            <!-- <div class="background-video">
                <video autoplay loop muted>
                    <source src="/Media/SpotyHomePageAnimation.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div> -->
            <div class="features-section">
                <h2 class="section-title">
                    <svg width="50px" height="50px">
                        <g>
                          <circle cx="25" cy="25" r="20" fill="#007BFF"></circle>
                          <text x="9" y="33" font-family="Arial" font-size="24" fill="#FFFFFF">⚙️</text> <!-- Gear icon -->
                        </g>
                      </svg>
                      Features
                </h2>
                <div class="features-container" id="features-container">
                    <!-- Features will be loaded here -->
                </div>
            </div>
        </section>
    </div>

    <script src="./Scripts/index.js"></script>
    <script src="./Scripts/navbar.js"></script>
</body>
</html> 