<?php
    //  Start the session at the very begining.
    session_start();

    // Include the database initialization file
    require_once '../PHP/DB/init_database.php';
    // include the admin utility file 
    require_once '../PHP/admin/utils.php';


    // Function to verify the Session exists
    function verifySession(){
        return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
    }

    // Redirect user to index page when trying to access admin panel without login
    if(!verifySession()){
        header("Location: /");
        exit;
    }

    // User verification on database
    if(!UserExists($_SESSION["user_id"],$PDO)){
        session_destroy();
        header("Location: index.php");
        exit;
    }

    // Check if current user is admin
    if(!isAdmin($_SESSION["user_id"])){
        header("Location: /");
        exit;
    }

    // Handle delete user request
    if (isset($_POST['delete_user_id']) && isAdmin($_SESSION["user_id"]) ) {
        $deleteUserId = $_POST['delete_user_id'];

        if(userExists($deleteUserId))
        {  
            // Execute the deleteUser function and store its state.
            $deleted = deleteUser($deleteUserId); 

            if($deleted) {
                echo  "<script>alert('User with id ".$deleteUserId." has been successful deleted.'); </script>";
                header('Refresh: 0;');
            }
        
            if(!$deleted){
                echo "<script>alert('User with id ".$deleteUserId." cannot be deleted.'); </script>";
                }
        }
    }
    
    try {
        // Fetch users from the database
        $stmt = $PDO->query("SELECT id, username, avatar, access_token, last_login, premium FROM users");
        $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        die("Database error: " . $e->getMessage());
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spoty - Admin Panel</title>
    <link rel="stylesheet" href="../CSS/index.css">
    <link rel="stylesheet" href="../CSS/admin.css">
    <link rel="stylesheet" href="../CSS/navbar.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    </head>
<body>
    <?php include_once("../navBar/index.php");?>

    <div class="admin-container">
        <h1>Spoty - Admin Panel</h1>
        <h2>Users of Spoty</h2>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Index</th>
                    <th>User ID</th>
                    <th>User</th>
                    <th>Access Token</th>
                    <th>Last Login</th>
                    <th>Premium State</th>
                </tr>
            </thead>
            <tbody>
                <?php
                 if(!empty($users))
                    {   $index = 1; 
                        foreach($users as $user){ ?>
                         <tr>
                            <td> <?=$index++;?></td>
                            <td> <?= htmlspecialchars($user["id"]) ?></td>
                             <td>
                                <?php $AvatarURL="https://cdn.discordapp.com/avatars/".htmlspecialchars($user['id'])."/".htmlspecialchars($user['avatar']).".png"; ?>
                                <img class="user-avatar" src="<?=$AvatarURL;?>" alt="User Avatar">
                                <?= htmlspecialchars('@'.$user["username"])?>
                            </td>
                            <td> <?= htmlspecialchars($user["access_token"])?></td>
                            <td><?= htmlspecialchars($user["last_login"]);?></td>
                            <td> 
                                <?php if($user['premium'] == 1) { ?>
                                    <span style="color:#4caf50;">Yes <i class="fa fa-check" style="color:#4caf50;"></i></span>
                                <?php } else { ?>
                                    <span style="color:#f44336;">No  <i class="fa fa-times"  style="color:#f44336;"></i></span>
                                <?php } ?>
                            </td>
                            <?php
                                if(!isAdmin($user['id'])){
                            ?>
                                <td>
                                    <form method="post"  onsubmit="return confirm(`Are you sure you want to delete user id: <?= htmlspecialchars($user['id']) ?>?`);">
                                        <input type="hidden" name="delete_user_id" value="<?=$user['id'] ?>">
                                            <button class="delete-btn" type="submit">
                                                <i class="fa fa-trash-alt" style="color: #ff4d4d"></i> <!-- Use a trash icon from Font Awesome -->
                                            </button>
                                    </form>
                                </td>
                            <?php
                                }
                            ?>
                        </tr>
                   <?php }
                 }else {
                      echo "<td colspan=6> <h1> There's no user's on the database! </h1> </td> ";
                  }   
                  ?>
            </tbody>
        </table>
    </div>
</body>
<script src="../Scripts/navbar.js"></script>
</html>