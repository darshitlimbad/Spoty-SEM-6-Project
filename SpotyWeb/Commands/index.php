<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spoty - Commands</title>
    <link rel="stylesheet" href="../CSS/index.css">
    <link rel="stylesheet" href="../CSS/table.css">
    <link rel="stylesheet" href="../CSS/navbar.css">
</head>
<body>
    <?php
        include_once("../navBar/index.php");
    ?>
    <div class="scroll-container">
        <section id="command" class="page">
            <div class="subscription-content">
                <h2 class="section-title">Commands</h2>
                <div class="table-container">
                    <table class="subscription-table">
                        <thead>
                            <tr>
                                <th>Command Name</th>
                                <th>Description</th>
                                <th>Plan</th>
                            </tr>
                        </thead>
                        <tbody id="all-commands-table-body">
                            <!-- Table rows will be dynamically loaded here via js-->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </div>
    <script src="../Scripts/commands.js"></script>
    <script src="../Scripts/navbar.js"></script>

</body>
</html>