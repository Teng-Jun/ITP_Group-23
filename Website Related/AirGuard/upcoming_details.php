<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Details - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="wrapper">
        <?php include 'header.php'; ?>
        <main>
            <a href="upcoming.php" class="back-button">Back to Upcoming Airdrops</a>
            <h2>Airdrop Details</h2>
            <div class="airdrop-details">
                <?php
                include 'dbconnection.php';

                $id = isset($_GET['id']) ? $_GET['id'] : '';
                $sql = "SELECT * FROM airdrops_data_speculative WHERE id = ?";

                $stmt = $conn->prepare($sql);
                $stmt->bind_param("i", $id); // Assuming 'id' is an integer
                $stmt->execute();
                $result = $stmt->get_result();

                if ($result->num_rows > 0) {
                    $row = $result->fetch_assoc();
                    echo '<div class="detail-item">';
                    echo '<img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="detail-logo">';
                    echo '<h3>' . htmlspecialchars($row['tle']) . '</h3>';
                    echo '<p>Platform: ' . htmlspecialchars($row['Platform']) . '</p>';
                    echo '<p>Status: ' . htmlspecialchars($row['Status']) . '</p>';
                    echo '<p>Features: ' . htmlspecialchars($row['Features']) . '</p>';
                    $guide = htmlspecialchars($row['Guide']);
                    $guide = str_replace(['[', ']'], '', $guide); // Removes square brackets
                    echo '<p>Guide: ' . $guide . '</p>';
                    echo '<p>Total Value: ' . htmlspecialchars($row['Total_Value']) . '</p>';
                    echo '<p>Requirements: ' . htmlspecialchars($row['Requirements']) . '</p>';
                    echo '<p>Number of Previous Drops: ' . htmlspecialchars($row['Num_Of_Prev_Drops']) . '</p>';
                    echo '<p><a href="' . htmlspecialchars($row['Website']) . '">Project Website</a></p>';
                    echo '<p><a href="' . htmlspecialchars($row['Whitepaper']) . '">Whitepaper</a></p>';
                    echo '<p>Facebook: ' . htmlspecialchars($row['Facebook']) . '</p>';
                    echo '<p>Telegram Group: ' . htmlspecialchars($row['Telegram Group']) . '</p>';
                    echo '</div>';
                } else {
                    echo "Airdrop details not found.";
                }
                $stmt->close();
                $conn->close();
                ?>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>