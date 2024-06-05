<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upcoming Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="wrapper">
        <?php include 'header.php'; ?>
        <main>
            <h2>Upcoming Airdrops</h2>
            <section id="search">
                <form action="upcoming.php" method="GET" align="center">
                    <input type="text" name="search" placeholder="Search for airdrops..." aria-label="Search Airdrops">
                    <select name="status">
                        <option value="">All Statuses</option>
                        <option value="Airdrop Confirmed">Confirmed</option>
                        <option value="Airdrop Unconfirmed">Unconfirmed</option>
                        <option value="Airdrop Expired">Expired</option>
                    </select>
                    <button type="submit">Search</button>
                    <button type="button" id="resetButton">Reset</button>
                </form>
            </section>
            <div class="airdrop-container">
                <?php
                include 'dbconnection.php';

                $search = isset($_GET['search']) ? $_GET['search'] : '';
                $status = isset($_GET['status']) ? $_GET['status'] : '';

                $sql = "SELECT tle, Platform, Status, Thumbnail FROM airdrops_data_speculative";
                $conditions = [];
                $params = [];
                $types = '';

                if ($search !== '') {
                    $conditions[] = "LOWER(tle) LIKE LOWER(?)";
                    $params[] = '%' . strtolower($search) . '%';
                    $types .= 's';  // string
                }

                if ($status !== '') {
                    $conditions[] = "Status = ?";
                    $params[] = $status;
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
                        echo '<img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="airdrop-logo">';
                        echo '<div class="airdrop-info">';
                        echo '<h3>' . htmlspecialchars($row['tle']) . '</h3>';
                        echo '<p>Platform: ' . htmlspecialchars($row['Platform']) . '</p>';
                        echo '<p>Status: <span class="' . ($row['Status'] == 'Airdrop Confirmed' ? 'status-confirmed' : ($row['Status'] == 'Airdrop Unconfirmed' ? 'status-pending' : 'status-expired')) . '">' . htmlspecialchars($row['Status']) . '</span></p>';
                        echo '</div>';
                        echo '</div>';
                    }
                } else {
                    echo "No upcoming airdrops found";
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