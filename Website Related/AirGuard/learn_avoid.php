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

        .pagination {
            display: flex;
            justify-content: center;
            padding: 20px;
        }

        .pagination a {
            color: black;
            padding: 8px 16px;
            text-decoration: none;
            transition: background-color .3s;
        }

        .pagination a.active {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }

        .pagination a:hover:not(.active) {
            background-color: #ddd;
            border-radius: 5px;
        }

        .search-bar {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
            width: 100%;
        }

        .search-bar input[type="text"] {
            width: 300px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-right: 10px;
        }

        .search-bar button {
            padding: 10px 20px;
            background-color: #007BFF;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }

        .search-bar button:hover {
            background-color: #0056b3;
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
            <div class="search-bar">
                <form action="learn_avoid.php" method="GET">
                    <input type="text" name="search" placeholder="Search by name..." value="<?php echo htmlspecialchars(isset($_GET['search']) ? $_GET['search'] : ''); ?>">
                    <button type="submit">Search</button>
                </form>
            </div>
            <div class="container">
                <?php
                include 'dbconnection.php';

                $results_per_page = 15;
                $search = isset($_GET['search']) ? $conn->real_escape_string($_GET['search']) : '';
                $sql = "SELECT COUNT(*) AS total FROM learnandavoid WHERE name LIKE '%$search%'";
                $result = $conn->query($sql);
                $row = $result->fetch_assoc();
                $total_results = $row['total'];
                $total_pages = ceil($total_results / $results_per_page);

                $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
                $start_from = ($page - 1) * $results_per_page;

                $sql = "SELECT * FROM learnandavoid WHERE name LIKE '%$search%' LIMIT $start_from, $results_per_page";
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
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
                ?>
            </div>
            <div class="pagination">
                <?php
                if ($page > 1) {
                    echo "<a href='learn_avoid.php?page=1&search=" . urlencode($search) . "'>&laquo; First</a>";
                    echo "<a href='learn_avoid.php?page=" . ($page - 1) . "&search=" . urlencode($search) . "'>&lsaquo; Previous</a>";
                }

                if ($total_pages <= 5) {
                    for ($i = 1; $i <= $total_pages; $i++) {
                        if ($i == $page) {
                            echo "<a class='active' href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                        } else {
                            echo "<a href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                        }
                    }
                } else {
                    if ($page <= 3) {
                        for ($i = 1; $i <= 5; $i++) {
                            if ($i == $page) {
                                echo "<a class='active' href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                            } else {
                                echo "<a href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search)     . "'>" . $i . "</a>";
                            }
                        }
                        echo "<a class='disabled'>...</a>";
                        echo "<a href='learn_avoid.php?page=" . $total_pages . "&search=" . urlencode($search) . "'>" . $total_pages . "</a>";
                    } elseif ($page > 3 && $page < $total_pages - 2) {
                        echo "<a href='learn_avoid.php?page=1&search=" . urlencode($search) . "'>1</a>";
                        echo "<a class='disabled'>...</a>";
                        for ($i = $page - 2; $i <= $page + 2; $i++) {
                            if ($i == $page) {
                                echo "<a class='active' href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                            } else {
                                echo "<a href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                            }
                        }
                        echo "<a class='disabled'>...</a>";
                        echo "<a href='learn_avoid.php?page=" . $total_pages . "&search=" . urlencode($search) . "'>" . $total_pages . "</a>";
                    } else {
                        echo "<a href='learn_avoid.php?page=1&search=" . urlencode($search) . "'>1</a>";
                        echo "<a class='disabled'>...</a>";
                        for ($i = $total_pages - 4; $i <= $total_pages; $i++) {
                            if ($i == $page) {
                                echo "<a class='active' href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                            } else {
                                echo "<a href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
                            }
                        }
                    }
                }

                if ($page < $total_pages) {
                    echo "<a href='learn_avoid.php?page=" . ($page + 1) . "&search=" . urlencode($search) . "'>Next &rsaquo;</a>";
                    echo "<a href='learn_avoid.php?page=" . $total_pages . "&search=" . urlencode($search) . "'>Last &raquo;</a>";
                }
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
