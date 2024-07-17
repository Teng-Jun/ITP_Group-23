<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learn & Avoid Airdrop Scams</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .card {
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            width: 300px;
            margin: 20px;
            height: 400px; /* Adjust the height as needed */
            display: flex;
            flex-direction: column;
            align-items: center; /* Center the content horizontally */
            padding: 20px; /* Add some padding */
        }
        .card img {
            width: 150px; /* Thumbnail size */
            height: 150px; /* Thumbnail size */
            object-fit: cover;
            border-radius: 50%; /* Make the image circular */
            margin-bottom: 10px; /* Add some space below the image */
        }
        .card-content {
            text-align: center; /* Center the text */
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center; /* Center the content horizontally */
        }
        .card-content h3 {
            margin: 0;
            font-size: 1.2em;
        }
        .card-content p {
            margin: 10px 0;
        }
        .card-content a {
            color: #007BFF;
            text-decoration: none;
            word-break: break-all; /* Ensure URLs break properly */
        }
        .card-content a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <?php include 'header.php'; ?>
        <main>
            <h2>Airdrop Scam Victims from Reddit Forum Threads</h2>
            <div class="container">
                <?php
                include 'dbconnection.php';
                $sql = "SELECT * FROM learnandavoid";
                $result = $conn->query($sql);
                if ($result->num_rows > 0) {
                    while($row = $result->fetch_assoc()) {
                        echo '<div class="card">';
                        echo '<img src="' . htmlspecialchars($row['image']) . '" alt="' . htmlspecialchars($row['name']) . '">';
                        echo '<div class="card-content">';
                        echo '<h3>' . htmlspecialchars($row['name']) . '</h3>';
                        echo '<p>Reddit URL: <a href="' . htmlspecialchars($row['reddit_url']) . '" target="_blank">' . htmlspecialchars($row['reddit_url']) . '</a></p>';
                        echo '<p>Official Website: <a href="' . htmlspecialchars($row['Official_Website']) . '" target="_blank">' . htmlspecialchars($row['Official_Website']) . '</a></p>';
                        echo '<p>Twitter: <a href="' . htmlspecialchars($row['Twitter']) . '" target="_blank">' . htmlspecialchars($row['Twitter']) . '</a></p>';
                        echo '<p>Facebook: <a href="' . htmlspecialchars($row['Facebook']) . '" target="_blank">' . htmlspecialchars($row['Facebook']) . '</a></p>';
                        echo '<p>Reddit: <a href="' . htmlspecialchars($row['Reddit']) . '" target="_blank">' . htmlspecialchars($row['Reddit']) . '</a></p>';
                        echo '</div>';
                        echo '</div>';
                    }
                } else {
                    echo '<p>No scam data available.</p>';
                }
                $conn->close();
                ?>
            </div>
        </main>
    </div>
</body>
</html>
