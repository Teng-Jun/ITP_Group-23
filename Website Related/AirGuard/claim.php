<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unique Airdrop Guides - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="wrapper">
        <?php include 'header.php'; ?>
        <main>
            <h2>How to claim Airdrops</h2>
            <section id="search">
                <form action="claim.php" method="GET" align="center">
                    <input type="text" name="search" placeholder="Search for airdrops..." aria-label="Search Airdrops">
                    <button type="submit">Search</button>
                    <button type="button" id="resetButton">Reset</button>
                </form>
            </section>
            <div class="airdrop-container">
                <?php
                    include 'dbconnection.php';

                    $search = isset($_GET['search']) ? $_GET['search'] : '';

                    $sql = "SELECT DISTINCT tle, Guide FROM airdrops_data_speculative";
                    $conditions = [];
                    $params = [];
                    $types = '';

                    if ($search !== '') {
                        $conditions[] = "LOWER(tle) LIKE LOWER(?)";
                        $params[] = '%' . strtolower($search) . '%';
                        $types .= 's';  // string
                    }

                    if (!empty($conditions)) {
                        $sql .= " WHERE " . join(" AND ", $conditions);
                    }

                    $stmt = $conn->prepare($sql);

                    if (!empty($params)) {
                        $stmt->bind_param($types, ...$params);
                    }

                    $stmt->execute();
                    $result = $stmt->get_result();

                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            echo '<div class="airdrop-item">';
                            echo '<img src="placeholder.jpg" alt="Token Logo" class="airdrop-logo">';
                            echo '<div class="airdrop-info">';
                            echo '<h3>' . htmlspecialchars($row['tle']) . '</h3>';
                            if ($row['Guide']) {  // Checking if the Guide field is not empty
                                $guideSteps = unserialize($row['Guide']);  // Unserializing the guide
                                echo '<ul>';
                                foreach ($guideSteps as $step) {
                                    echo '<li>' . htmlspecialchars($step) . '</li>';
                                }
                                echo '</ul>';
                            } else {
                                echo '<p>No guide available.</p>';
                            }
                            echo '</div>';
                            echo '</div>';
                        }
                    } else {
                        echo "No unique airdrop guides found";
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