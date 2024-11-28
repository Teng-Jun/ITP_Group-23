<?php
// Include database connection
include 'dbconnection.php';

// Pagination Settings
$recordsPerPage = 10; // Number of records per page
$currentPage = isset($_GET['page']) && is_numeric($_GET['page']) ? (int)$_GET['page'] : 1;
$offset = ($currentPage - 1) * $recordsPerPage;

// Retrieve and sanitize GET parameters
$search = isset($_GET['search']) ? trim($_GET['search']) : '';
$risk_score = isset($_GET['risk_score']) ? trim($_GET['risk_score']) : '';
$sort = isset($_GET['sort']) ? trim($_GET['sort']) : ''; // No sort by default

// Validate sort parameter
if ($sort !== 'asc' && $sort !== 'desc') {
    $sort = ''; // Reset to default if invalid
}

// Base SQL query for counting total records
$countSql = "SELECT COUNT(*) as total FROM airdrops_data WHERE Status = 'Airdrop Confirmed'";
$countConditions = [];
$countParams = [];
$countTypes = '';

// Add search condition if applicable
if ($search !== '') {
    $countConditions[] = "LOWER(Title) LIKE LOWER(?)";
    $countParams[] = '%' . strtolower($search) . '%';
    $countTypes .= 's';  // string
}

// Add risk score conditions if applicable
if ($risk_score !== '') {
    // Assuming Probability is stored as a decimal (0-1)
    if ($risk_score == 'low') {
        $countConditions[] = "Probability < 0.01"; // <1%
    } elseif ($risk_score == 'medium') {
        $countConditions[] = "Probability >= 0.01 AND Probability <= 0.50"; // 1% - 50%
    } elseif ($risk_score == 'high') {
        $countConditions[] = "Probability > 0.50"; // >50%
    }
}

// Append conditions to count SQL query
if (!empty($countConditions)) {
    $countSql .= " AND " . implode(" AND ", $countConditions);
}

// Prepare and execute the count SQL statement
$countStmt = $conn->prepare($countSql);
if ($countStmt === false) {
    die('Prepare failed: ' . htmlspecialchars($conn->error));
}

if (!empty($countParams)) {
    $countStmt->bind_param($countTypes, ...$countParams);
}

$countStmt->execute();
$countResult = $countStmt->get_result();
$totalAirdrops = $countResult->fetch_assoc()['total'];
$countStmt->close();

// Calculate total pages
$totalPages = ceil($totalAirdrops / $recordsPerPage);

// Base SQL query for fetching records with LIMIT and OFFSET
$sql = "SELECT * FROM airdrops_data WHERE Status = 'Airdrop Confirmed'";
$conditions = [];
$params = [];
$types = '';

// Add search condition if applicable
if ($search !== '') {
    $conditions[] = "LOWER(Title) LIKE LOWER(?)";
    $params[] = '%' . strtolower($search) . '%';
    $types .= 's';  // string
}

// Add risk score conditions if applicable
if ($risk_score !== '') {
    // Assuming Probability is stored as a decimal (0-1)
    if ($risk_score == 'low') {
        $conditions[] = "Probability < 0.01"; // <1%
    } elseif ($risk_score == 'medium') {
        $conditions[] = "Probability >= 0.01 AND Probability <= 0.50"; // 1% - 50%
    } elseif ($risk_score == 'high') {
        $conditions[] = "Probability > 0.50"; // >50%
    }
}

// Append conditions to SQL query
if (!empty($conditions)) {
    $sql .= " AND " . implode(" AND ", $conditions);
}

// Append ORDER BY clause based on sort parameter
if ($sort === 'asc') {
    $sql .= " ORDER BY Probability ASC";
} elseif ($sort === 'desc') {
    $sql .= " ORDER BY Probability DESC";
}
// Else, no specific order (default as stored in DB)

// Append LIMIT and OFFSET for pagination
$sql .= " LIMIT ? OFFSET ?";
$params[] = $recordsPerPage;
$params[] = $offset;
$types .= 'ii'; // integer for LIMIT and OFFSET

// Prepare and execute the SQL statement
$stmt = $conn->prepare($sql);

if ($stmt === false) {
    die('Prepare failed: ' . htmlspecialchars($conn->error));
}

if (!empty($params)) {
    $stmt->bind_param($types, ...$params);
}

$stmt->execute();
$result = $stmt->get_result();

// Fetch all tokens
$tokens = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        // Multiply Probability by 100 to make it a percentage
        $riskScore = $row['Probability'] * 100;

        // Format the risk score
        if ($riskScore < 0.01) {
            $riskScoreDisplay = '<0.01%';
        } elseif ($riskScore > 99.9) {
            $riskScoreDisplay = '>99.9%';
        } else {
            // Round to two decimal places for better readability
            $riskScoreDisplay = number_format($riskScore, 2) . '%';
        }

        $tokens[] = [
            'id' => $row['id'],
            'airdrop_name' => $row['Title'],
            'Thumbnail' => $row['Thumbnail'],
            'Platform' => $row['Platform'],
            'RiskScore' => $riskScoreDisplay,
            'Status' => $row['Status'],
            'positive_percentage' => $row['positive_percentage'],
            'negative_percentage' => $row['negative_percentage']
        ];
    }
}
$stmt->close();
$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Current Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- Font Awesome for icons (if needed elsewhere) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper">
        <main>
            <h2>Current Airdrops</h2>
            <div class="container">
                <section id="search">
                    <form action="current.php" method="GET" class="form-inline justify-content-center mb-4 w-100">
                        <!-- Search Input -->
                        <input type="text" name="search" class="form-control mr-2 mb-2" placeholder="Search for airdrops..." aria-label="Search Airdrops" value="<?php echo htmlspecialchars($search ?? ''); ?>">
                        
                        <!-- Risk Score Dropdown -->
                        <select name="risk_score" class="form-control mr-2 mb-2">
                            <option value="">All Risk Scores</option>
                            <option value="low" <?php if (isset($risk_score) && $risk_score == 'low') echo 'selected'; ?>>Low (&lt; 1%)</option>
                            <option value="medium" <?php if (isset($risk_score) && $risk_score == 'medium') echo 'selected'; ?>>Medium (1% - 50%)</option>
                            <option value="high" <?php if (isset($risk_score) && $risk_score == 'high') echo 'selected'; ?>>High (&gt; 50%)</option>
                        </select>
                        
                        <!-- Search and Reset Buttons -->
                        <button type="submit" class="btn btn-primary mr-2 mb-2">Search</button>
                        <button type="button" class="btn btn-success mb-2" id="resetButton">Reset</button>
                        
                        <!-- Total Airdrops Display -->
                        <div class="ml-auto mb-2 total-airdrops-container">
                            <p class="mb-0"><strong>Total Airdrops:</strong> <?php echo $totalAirdrops; ?></p>
                        </div>
                    </form>
                </section>
                
                <div class="airdrop-container">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Asset</th>
                                <th>Chain</th>
                                <th>
                                    Risk Score
                                    <!-- Sort Button as Image -->
                                    <a href="?<?php
                                        // Build query string for sorting
                                        $query = $_GET;
                                        // Determine the next sort order
                                        if ($sort === 'asc') {
                                            $query['sort'] = 'desc';
                                        } else {
                                            $query['sort'] = 'asc';
                                        }
                                        echo htmlspecialchars(http_build_query($query));
                                    ?>" class="sort-icon" title="Sort Risk Score">
                                        <!-- Image for sort button -->
                                        <img src="image/sorting.png" alt="Sort Risk Score" width="20" height="20">
                                    </a>
                                </th>
                                <th>Status</th>
                                <th>Sentiment</th>
                            </tr>
                        </thead>
                        <tbody id="token-list">
                            <?php
                            if (!empty($tokens)) {
                                $index = $offset + 1; // Continuous numbering across pages
                                foreach ($tokens as $row) {
                                    echo '<tr>';
                                    echo '<td>' . $index++ . '</td>';
                                    echo '<td><a href="upcoming_details.php?id=' . htmlspecialchars($row['id']) . '" class="airdrop-item-link"><img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="upcomingtoken-logo"> ' . htmlspecialchars($row['airdrop_name']) . '</a></td>';
                                    echo '<td>' . htmlspecialchars($row['Platform']) . '</td>';
                                    echo '<td>' . htmlspecialchars($row['RiskScore']) . '</td>';
                                    echo '<td class="' . ($row['Status'] == 'Airdrop Confirmed' ? 'status-confirmed' : ($row['Status'] == 'Airdrop Unconfirmed' ? 'status-pending' : 'status-expired')) . '">' . htmlspecialchars($row['Status']) . '</td>';
                                    echo '<td>';
                                    echo '<div class="custom-legend">';
                                    echo '<div class="custom-legend-item">';
                                    echo '<div class="custom-legend-color" style="background-color: #36a2eb;"></div>';
                                    echo 'Positive: ' . htmlspecialchars($row['positive_percentage']) . '%';
                                    echo '</div>';
                                    echo '<div class="custom-legend-item">';
                                    echo '<div class="custom-legend-color" style="background-color: #ff6384;"></div>';
                                    echo 'Negative: ' . htmlspecialchars($row['negative_percentage']) . '%';
                                    echo '</div>';
                                    echo '</div>';
                                    echo '</td>';
                                    echo '</tr>';
                                }
                            } else {
                                echo '<tr><td colspan="6" class="text-center">No current airdrops found</td></tr>';
                            }
                            ?>
                        </tbody>
                    </table>
                </div>
    
                <!-- Pagination Controls -->
                <?php if ($totalPages > 1): ?>
                    <nav aria-label="Page navigation example">
                        <ul class="pagination justify-content-center">
                            <!-- Previous Page Link -->
                            <li class="page-item <?php if ($currentPage <= 1) echo 'disabled'; ?>">
                                <a class="page-link" href="?<?php
                                    $query = $_GET;
                                    $query['page'] = $currentPage - 1;
                                    echo htmlspecialchars(http_build_query($query));
                                ?>" tabindex="-1">Previous</a>
                            </li>
    
                            <!-- Page Number Links -->
                            <?php
                            // Define the range of pages to show
                            $range = 2; // Show 2 pages before and after current page
                            for ($i = max(1, $currentPage - $range); $i <= min($totalPages, $currentPage + $range); $i++):
                            ?>
                                <li class="page-item <?php if ($i == $currentPage) echo 'active'; ?>">
                                    <a class="page-link" href="?<?php
                                        $query = $_GET;
                                        $query['page'] = $i;
                                        echo htmlspecialchars(http_build_query($query));
                                    ?>"><?php echo $i; ?></a>
                                </li>
                            <?php endfor; ?>
    
                            <!-- Next Page Link -->
                            <li class="page-item <?php if ($currentPage >= $totalPages) echo 'disabled'; ?>">
                                <a class="page-link" href="?<?php
                                    $query = $_GET;
                                    $query['page'] = $currentPage + 1;
                                    echo htmlspecialchars(http_build_query($query));
                                ?>">Next</a>
                            </li>
                        </ul>
                    </nav>
                <?php endif; ?>
    
            </div>
        </main>
    </div>
    <!-- Footer -->
    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>
    
    <!-- JavaScript Section -->
    <script src="script.js"></script>
    <script>
        // Removed the JavaScript that manipulates the table to prevent layout issues.
        // Since PHP is handling the table rendering, additional JavaScript manipulation is unnecessary.

        // Reset button functionality
        document.getElementById('resetButton').addEventListener('click', () => {
            window.location.href = 'current.php';
        });
    </script>
    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
