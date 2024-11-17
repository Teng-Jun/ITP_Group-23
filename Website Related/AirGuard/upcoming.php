<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upcoming Airdrops - Airdrop Tracker</title>
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
            <h2>Upcoming Airdrops</h2>
            <div class="container">
                <section id="search">
                    <form action="upcoming.php" method="GET" align="center">
                        <input type="text" name="search" placeholder="Search for airdrops..." aria-label="Search Airdrops">
                        <select name="status">
                            <option value="">All Statuses</option>
                            <option value="Airdrop Unconfirmed">Unconfirmed</option>
                            <option value="n/a">Not Applicable</option>
                        </select>
                        <select name="risk_score">
                            <option value="">All Risk Scores</option>
                            <option value="low">Low (< 1%)</option>
                            <option value="medium">Medium (1% - 50%)</option>
                            <option value="high">High (> 50%)</option>
                        </select>
                        <button type="submit" class="btn btn-primary">Search</button>
                        <button type="button" class="btn btn-success" id="resetButton">Reset</button>
                    </form>
                </section>
                <div class="airdrop-container">
                    <table>
                        <thead>
                            <h2>Tokens List</h2>
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
                            include 'dbconnection.php';

                            $search = isset($_GET['search']) ? $_GET['search'] : '';
                            $status = isset($_GET['status']) ? $_GET['status'] : '';
                            $risk_score = isset($_GET['risk_score']) ? $_GET['risk_score'] : '';

                            $sql = "SELECT * FROM airdrops_data WHERE (Status = 'Airdrop Unconfirmed' OR Status = 'n/a')";
                            $conditions = [];
                            $params = [];
                            $types = '';

                            if ($search !== '') {
                                $conditions[] = "LOWER(Title) LIKE LOWER(?)";
                                $params[] = '%' . strtolower($search) . '%';
                                $types .= 's';  // string
                            }

                            if ($status !== '') {
                                $conditions[] = "Status = ?";
                                $params[] = $status;
                                $types .= 's';  // string
                            }

                            if ($risk_score !== '') {
                                if ($risk_score == 'low') {
                                    $conditions[] = "Probability < 1";
                                } elseif ($risk_score == 'medium') {
                                    $conditions[] = "Probability >= 1 AND Probability <= 50";
                                } elseif ($risk_score == 'high') {
                                    $conditions[] = "Probability > 50";
                                }
                            }

                            if (!empty($conditions)) {
                                $sql .= " AND " . join(" AND ", $conditions);
                            }

                            $stmt = $conn->prepare($sql);

                            if ($stmt === false) {
                                die('Prepare failed: ' . htmlspecialchars($conn->error));
                            }

                            if (!empty($params)) {
                                $stmt->bind_param($types, ...$params);
                            }

                            $stmt->execute();
                            $result = $stmt->get_result();

                            $tokens = [];

                            if ($result->num_rows > 0) {
                                $index = 1;
                                while ($row = $result->fetch_assoc()) {
                                    // Format the risk score
                                    $riskScore = $row['Probability'];
                                    if ($riskScore == 0) {
                                        $riskScoreDisplay = '<0.01%';
                                    } elseif ($riskScore == 100) {
                                        $riskScoreDisplay = '>99.9%';
                                    } else {
                                        $riskScoreDisplay = $riskScore . '%';
                                    }

                                    $tokens[] = [
                                        'id' => $row['id'],
                                        'airdrop_name' => $row['Title'],
                                        'Thumbnail' => $row['Thumbnail'],
                                        'Platform' => $row['Platform'],
                                        'RiskScore' => $riskScoreDisplay,
                                        'Status' => $row['Status'],
                                        'positive_percentage' => $row['positive_percentage'],
                                        'neutral_percentage' => $row['neutral_percentage'],
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
                                    echo '<div class="custom-legend-color" style="background-color: #ffcd56;"></div>';
                                    echo 'Neutral: ' . htmlspecialchars($row['neutral_percentage']) . '%';
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
                                echo '<tr><td colspan="6">No upcoming airdrops found</td></tr>';
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
            return fetch('data/sentiment_results_20241118_003834.json')
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
                                <div class="custom-legend-color" style="background-color: #ffcd56;"></div>
                                Neutral: ${parseFloat(token.neutral_percentage).toFixed(2)}%
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
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
