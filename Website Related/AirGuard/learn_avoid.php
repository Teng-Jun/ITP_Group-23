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
</head>
<body>
    <div class="learn_avoid-header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="learn_avoid-wrapper">
        <main class="learn_avoid-main">
            <h2>Airdrop Scam Victims from Reddit Forum Threads</h2>
            <p class="learn_avoid-disclaimer">
                Disclaimer: Users must exercise due diligence to determine the reliability of free airdrops or Web3 project tokens. We are not responsible for your actions taken based on this information. Be aware of the common saying about "rug pulls" in crypto, especially for new projects using airdrops to distribute free tokens. This data is provided based on Reddit discussions and vetted websites.
            </p>
            <div class="learn_avoid-search-bar">
                <form action="learn_avoid.php" method="GET">
                    <input type="text" name="search" placeholder="Search by name..." value="<?php echo htmlspecialchars(isset($_GET['search']) ? $_GET['search'] : ''); ?>">
                    <button type="submit">Search</button>
                </form>
            </div>
            <div class="learn_avoid-container">
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

                $sql = "SELECT id, name, image, reddit_url, Official_Website, Twitter, Facebook, Reddit, Instagram, Telegram, Discord FROM learnandavoid WHERE name LIKE '%$search%' LIMIT $start_from, $results_per_page";
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        echo '<div class="learn_avoid-card">';
                        echo '<img src="' . htmlspecialchars($row['image']) . '" alt="' . htmlspecialchars($row['name']) . '">';
                        echo '<div class="learn_avoid-card-content">';
                        echo '<h3>' . htmlspecialchars($row['name']) . '</h3>';
                        echo '<p>Reddit Discussion or Vetted Sites: &nbsp <a href="' . htmlspecialchars($row['reddit_url']) . '" target="_blank">' . htmlspecialchars($row['reddit_url']) . '</a></p>';
                        echo '<p>';
                        echo (!empty($row['Official_Website']) && strtolower($row['Official_Website']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Official_Website']) . '" target="_blank"><i class="fas fa-globe"></i></a>' : '<a class="disabled"><i class="fas fa-globe"></i></a>';
                        echo (!empty($row['Twitter']) && strtolower($row['Twitter']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Twitter']) . '" target="_blank"><i class="fab fa-twitter"></i></a>' : '<a class="disabled"><i class="fab fa-twitter"></i></a>';
                        echo (!empty($row['Facebook']) && strtolower($row['Facebook']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Facebook']) . '" target="_blank"><i class="fab fa-facebook-f"></i></a>' : '<a class="disabled"><i class="fab fa-facebook-f"></i></a>';
                        echo (!empty($row['Reddit']) && strtolower($row['Reddit']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Reddit']) . '" target="_blank"><i class="fab fa-reddit-alien"></i></a>' : '<a class="disabled"><i class="fab fa-reddit-alien"></i></a>';
                        echo (!empty($row['Instagram']) && strtolower($row['Instagram']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Instagram']) . '" target="_blank"><i class="fab fa-instagram"></i></a>' : '<a class="disabled"><i class="fab fa-instagram"></i></a>';
                        echo (!empty($row['Telegram']) && strtolower($row['Telegram']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Telegram']) . '" target="_blank"><i class="fab fa-telegram"></i></a>' : '<a class="disabled"><i class="fab fa-telegram"></i></a>';
                        echo (!empty($row['Discord']) && strtolower($row['Discord']) !== 'nan') ? '<a href="' . htmlspecialchars($row['Discord']) . '" target="_blank"><i class="fab fa-discord"></i></a>' : '<a class="disabled"><i class="fab fa-discord"></i></a>';
                        echo '</p>';
                        echo '</div>';
                        echo '</div>';
                    }
                } else {
                    echo '<p>No scam data available.</p>';
                }
                ?>
            </div>
            <div class="learn_avoid-pagination">
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
                                echo "<a href='learn_avoid.php?page=" . $i . "&search=" . urlencode($search) . "'>" . $i . "</a>";
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
         <!-- Add the footer include here -->
         <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>

