<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learn & Avoid Airdrop Scams</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .airdrop-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .airdrop-item {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin: 15px;
            width: 250px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            text-align: center;
            min-height: 200px;
        }
        .airdrop-logo {
            width: 100px;
            height: 100px;
            object-fit: contain;
            margin-bottom: 10px;
        }
        .airdrop-info {
            margin-top: 10px;
        }
        .airdrop-info p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <?php include 'header.php'; ?>
        <main>
            <h2>Airdrop Scam Victims from Reddit Forum Threads</h2>
            <section id="safety">
                <?php
                include 'dbconnection.php';

                $sql = "SELECT name, reddit_url, Official_Website, Twitter, Facebook, Reddit, image FROM learnandavoid";
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {
                    echo '<div class="airdrop-container">';
                    while($row = $result->fetch_assoc()) {
                        echo '<div class="airdrop-item">';
                        echo '<img src="' . htmlspecialchars($row['image']) . '" alt="Token Logo" class="airdrop-logo">';
                        echo '<div class="airdrop-info">';
                        echo '<h3>' . htmlspecialchars($row['name']) . '</h3>';
                        echo '<p><a href="' . htmlspecialchars($row['reddit_url']) . '" target="_blank">Reddit Forum</a></p>';
                        echo '<p><a href="' . htmlspecialchars($row['Official_Website']) . '" target="_blank">Official Website</a></p>';
                        echo '<p><a href="' . htmlspecialchars($row['Twitter']) . '" target="_blank">Twitter</a></p>';
                        echo '<p><a href="' . htmlspecialchars($row['Facebook']) . '" target="_blank">Facebook</a></p>';
                        echo '<p><a href="' . htmlspecialchars($row['Reddit']) . '" target="_blank">Reddit Website</a></p>';
                        echo '</div>';
                        echo '</div>';
                    }
                    echo '</div>';
                } else {
                    echo "No airdrop scams found.";
                }

                $conn->close();
                ?>
            </section>
        </main>
        <script src="script.js"></script>
    </div>
</body>
</html>
