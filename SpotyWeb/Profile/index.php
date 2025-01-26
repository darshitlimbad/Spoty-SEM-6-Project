<?php
    // Start the session if it's not already started
    if (session_status() == PHP_SESSION_NONE) {
        session_start();
    }

    // Check if user_id is set in the session (user is logged in)
    if (!isset($_SESSION['user_id'])) {
       header("Location: /PHP/index.php");
       exit();
    }

    // Load the configuration file
    $config_file = "../PHP/DB/config.json";
    if(!file_exists($config_file)){
        die("Config file missing!");
    }
    $config = json_decode(file_get_contents($config_file), true);

    // Database configuration
    $db_host = $config['database']['host'];
    $db_user = $config['database']['username'];
    $db_pass = $config['database']['password'];
    $db_name = $config['database']['dbname'];

    // Create connection
    $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Get the user_id from session
    $user_id = $_SESSION['user_id'];

    // SQL query to fetch user data
     $sql = "SELECT id, username, discriminator, avatar, premium, last_login FROM users WHERE id = ?";
     $stmt = $conn->prepare($sql);
     $stmt->bind_param("s", $user_id);
     $stmt->execute();
     $result = $stmt->get_result();

    $user = null;
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
    }

     // Close the database connection
    $stmt->close();
    $conn->close();

    if(!$user) {
        echo "User not found!";
        header("Location: /PHP/index.php");
        exit;
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spoty - Profile</title>
    <link rel="stylesheet" href="../CSS/index.css">
    <link rel="stylesheet" href="../CSS/table.css">
    <link rel="stylesheet" href="../CSS/navbar.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
    <?php include_once("../navBar/index.php");?>
    
    <div class="scroll-container">
        <section id="profile-section" class="page">
            <div class="subscription-content">
                 <h2 class="section-title">User Profile</h2>
                 <div class="table-container">
                    <table class="subscription-table">
                        <tbody>
                            <tr>
                                <td><strong>User ID:</strong></td>
                                <td><?php echo htmlspecialchars($user['id']); ?></td>
                            </tr>
                              <tr>
                                <td><strong>Username:</strong></td>
                                <td><?php echo htmlspecialchars($user['username']); ?></td>
                            </tr>
                            <tr>
                                <td><strong>Discriminator:</strong></td>
                                <td><?php echo htmlspecialchars($user['discriminator']); ?></td>
                            </tr>
                             <tr>
                                <td><strong>Last Login:</strong></td>
                                <td><?php echo htmlspecialchars($user['last_login']); ?></td>
                            </tr>
                              <tr>
                                <td><strong>Premium Member:</strong></td>
                                <td>
                                    <?php if($user['premium'] == 1) { ?>
                                        <span style="color:#4caf50;">Yes <i class="fa fa-check" style="color:#4caf50;"></i></span>
                                    <?php } else { ?>
                                       <span style="color:#f44336;">No  <i class="fa fa-times"  style="color:#f44336;"></i></span>
                                    <?php } ?>
                                </td>
                            </tr>
                            <tr>
                                <?php $AvatarURL="https://cdn.discordapp.com/avatars/".htmlspecialchars($user['id'])."/".htmlspecialchars($user['avatar']).".png"; ?>
                                <td><strong>Avatar:</strong></td>
                                <td><img src="<?php echo $AvatarURL?>" alt="User Avatar" style="max-width: 100px; border-radius:50%;"></td>
                            </tr>
                           
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
     </div>
    <script src="../Scripts/index.js"></script>
    <script src="../Scripts/navbar.js"></script>
</body>
</html>