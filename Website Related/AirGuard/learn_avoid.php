<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learn & Avoid Airdrop Scams</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <style>
        .wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 auto;
            padding: 1em;
            width: 100%;
        }

        main {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            max-width: 1200px;
            margin: 0 auto;
        }

        .card {
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            width: 300px;
            margin: 20px;
            height: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        .card img {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 50%;
            margin-bottom: 10px;
        }

        .card-content {
            text-align: center;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
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
            word-break: break-all;
            margin: 0 5px;
        }

        .card-content a.disabled {
            color: gray;
            pointer-events: none;
        }

        .card-content a:hover {
            text-decoration: underline;
        }

        .disclaimer {
            color: #ff0000;
            font-weight: bold;
            margin: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper">
        <main>
            <h2>Airdrop Scam Victims from Reddit Forum Threads</h2>
            <p class="disclaimer">
                Disclaimer: Users must exercise due diligence to determine the reliability of free airdrops or Web3 project tokens. We are not responsible for your actions taken based on this information. Be aware of the common saying about "rug pulls" in crypto, especially for new projects using airdrops to distribute free tokens. This data is provided based on Reddit discussions and vetted websites.
            </p>
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
                        echo '<p>Reddit Discussion or Vetted Sites: &nbsp <a href="' . htmlspecialchars($row['reddit_url']) . '" target="_blank">' . htmlspecialchars($row['reddit_url']) . '</a></p>';
                        echo '<p>';
                        echo !empty($row['Official_Website']) ? '<a href="' . htmlspecialchars($row['Official_Website']) . '" target="_blank"><i class="fas fa-globe"></i></a>' : '<a class="disabled"><i class="fas fa-globe"></i></a>';
                        echo !empty($row['Twitter']) ? '<a href="' . htmlspecialchars($row['Twitter']) . '" target="_blank"><i class="fab fa-twitter"></i></a>' : '<a class="disabled"><i class="fab fa-twitter"></i></a>';
                        echo !empty($row['Facebook']) ? '<a href="' . htmlspecialchars($row['Facebook']) . '" target="_blank"><i class="fab fa-facebook-f"></i></a>' : '<a class="disabled"><i class="fab fa-facebook-f"></i></a>';
                        echo !empty($row['Reddit']) ? '<a href="' . htmlspecialchars($row['Reddit']) . '" target="_blank"><i class="fab fa-reddit-alien"></i></a>' : '<a class="disabled"><i class="fab fa-reddit-alien"></i></a>';
                        echo '</p>';
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
        <script src="script.js"></script>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
