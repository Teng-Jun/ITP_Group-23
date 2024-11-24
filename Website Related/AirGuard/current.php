<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Current Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
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
                    <form action="current.php" method="GET" class="form-inline justify-content-center">
                        <input type="text" name="search" class="form-control mr-2 mb-2" placeholder="Search for airdrops..." aria-label="Search Airdrops" value="<?php echo htmlspecialchars($search ?? ''); ?>">
                        <select name="risk_score" class="form-control mr-2 mb-2">
                            <option value="">All Risk Scores</option>
                            <option value="low" <?php if (isset($risk_score) && $risk_score == 'low') echo 'selected'; ?>>Low (&lt; 1%)</option>
                            <option value="medium" <?php if (isset($risk_score) && $risk_score == 'medium') echo 'selected'; ?>>Medium (1% - 50%)</option>
                            <option value="high" <?php if (isset($risk_score) && $risk_score == 'high') echo 'selected'; ?>>High (&gt; 50%)</option>
                        </select>
                        <button type="submit" class="btn btn-primary mr-2 mb-2">Search</button>
                        <button type="button" class="btn btn-success mb-2" id="resetButton">Reset</button>
                    </form>
                </section>
                
                <?php
                // Include database connection
                include 'dbconnection.php';

                // Retrieve and sanitize GET parameters
                $search = isset($_GET['search']) ? trim($_GET['search']) : '';
                $risk_score = isset($_GET['risk_score']) ? trim($_GET['risk_score']) : '';

                // Base SQL query
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

                // Calculate total number of airdrops retrieved
                $totalAirdrops = $result->num_rows;
                ?>

                <!-- Display total number of airdrops on the top right corner -->
                <div class="d-flex justify-content-end mb-3">
                    <p class="total-airdrops mb-0"><strong>Total Airdrops:</strong> <?php echo $totalAirdrops; ?></p>
                </div>

                <div class="airdrop-container">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Asset</th>
                                <th>Chain</th>
                                <th>Risk Score</th>
                                <th>Status</th>
                                <th>Sentiment</th>
                            </tr>
                        </thead>
                        <tbody id="token-list">
                            <?php
                            $tokens = [];

                            if ($result->num_rows > 0) {
                                $index = 1;
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

                                    echo '<tr>';
                                    echo '<td>' . $index++ . '</td>';
                                    echo '<td><a href="upcoming_details.php?id=' . htmlspecialchars($row['id']) . '" class="airdrop-item-link"><img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="upcomingtoken-logo"> ' . htmlspecialchars($row['Title']) . '</a></td>';
                                    echo '<td>' . htmlspecialchars($row['Platform']) . '</td>';
                                    echo '<td>' . htmlspecialchars($riskScoreDisplay) . '</td>';
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
                            $stmt->close();
                            $conn->close();
                            ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>
    <!-- Add the footer include here -->
    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>
    <script src="script.js"></script>
    <script>
        let sentimentData = [];
        let tokenData = <?php echo json_encode($tokens); ?>;

        // Function to fetch sentiment data from JSON file
        function fetchSentimentData() {
            return fetch('data/roberta_sentiment_results.json')
                .then(response => response.json())
                .then(data => {
                    sentimentData = data;
                    console.log("Sentiment data fetched successfully", sentimentData);
                    mergeData();
                })
                .catch(error => console.error('Error fetching sentiment data:', error));
        }

        // Function to merge sentiment data and token data
        function mergeData() {
            tokenData = tokenData.map(token => {
                const sentiment = sentimentData.find(s => s.airdrop_name === token.airdrop_name);
                return {
                    ...token,
                    ...sentiment
                };
            });
            displayTokens(tokenData);
        }

        // Function to display tokens
        function displayTokens(tokens) {
            const tokenList = document.getElementById('token-list');
            tokenList.innerHTML = ''; // Clear current list

            tokens.forEach((token, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td><a href="upcoming_details.php?id=${token.id}" class="airdrop-item-link"><img src="${token.Thumbnail}" alt="Token Logo" class="token-logo"> ${token.airdrop_name}</a></td>
                    <td>${token.Platform}</td>
                    <td>${token.RiskScore}</td>
                    <td class="${token.Status === 'Airdrop Confirmed' ? 'status-confirmed' : (token.Status === 'Airdrop Unconfirmed' ? 'status-pending' : 'status-expired')}">${token.Status}</td>
                    <td>
                        <div class="custom-legend">
                            <div class="custom-legend-item">
                                <div class="custom-legend-color" style="background-color: #36a2eb;"></div>
                                Positive: ${parseFloat(token.positive_percentage).toFixed(2)}%
                            </div>
                            <div class="custom-legend-item">
                                <div class="custom-legend-color" style="background-color: #ff6384;"></div>
                                Negative: ${parseFloat(token.negative_percentage).toFixed(2)}%
                            </div>
                        </div>
                    </td>
                `;
                tokenList.appendChild(row);
            });
        }

        // Fetch data on page load
        document.addEventListener('DOMContentLoaded', () => {
            fetchSentimentData();
        });

        // Reset button functionality
        document.getElementById('resetButton').addEventListener('click', () => {
            window.location.href = 'current.php';
        });
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
