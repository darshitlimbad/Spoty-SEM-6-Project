<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Spoty - Subscription Plans</title>
    <link rel="stylesheet" href="../CSS/index.css">
    <link rel="stylesheet" href="../CSS/subscriptionPage.css">
    <link rel="stylesheet" href="../CSS/navbar.css">
</head>
<body>
  <?php
    include_once("../navBar/index.php");
  ?>
  <div class="scroll-container">
    <section id="subscription-page" class="page">
        <div class="subscription-content">
            <h2 class="section-title">Subscription Plans</h2>
            <div class="plans-container">
                <div class="plan-card">
                    <h3>Free Plan</h3>
                     <ul>
                        <li>Basic Music Playback</li>
                         <li>Queue Management</li>
                        <li>Access to all music platforms</li>
                    </ul>
                    <button class="btn btn-free" disabled>Current Plan</button>
                </div>
                <div class="plan-card premium">
                    <h3>Premium Plan</h3>
                    <ul>
                         <li>All the features of Free plan</li>
                         <li>24/7 Uptime</li>
                         <li>High Audio Quality</li>
                         <li>Ad-Free Experience</li>
                         <li>Priority Support</li>
                         <li>Playlist support</li>
                          <li>Skip to a specific song using index</li>
                           <li>Repeat current song</li>
                           <li>Control volume level</li>
                    </ul>
                    <button class="btn btn-premium" id="btnSubscribe"> Upgrade to Premium </button>
                </div>
            </div>
        </div>
      </section>
    </div>
  <script src="../Scripts/navbar.js"></script>
  <script src="../Scripts/subscription.js"></script>
</body>
</html>