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
                            <option value="Airdrop Confirmed">Confirmed</option>
                            <option value="Airdrop Unconfirmed">Unconfirmed</option>
                            <option value="Airdrop Expired">Expired</option>
                        </select>
                        <button type="submit" class="btn btn-primary">Search</button>
                        <button class="btn btn-success" id="resetButton">Reset</button>
                    </form>
                </section>
                <div class="tabs">
                    <button id="most-scanned" class="tab-button" onclick="filterTokens('most-scanned')">Tokens: Most Scanned</button>
                    <button id="dangerous-threats" class="tab-button" onclick="filterTokens('dangerous-threats')">Tokens: Dangerous Threats</button>
                    <button id="requirements-need" class="tab-button" onclick="filterTokens('requirements-need')">Tokens: Requirements Need</button>
                </div>
                <div class="airdrop-container">
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
                                    <th>Requirements</th>
                                    <th>Whitepaper</th>
                                    <th colspan="3" class="social-media-header">Social Media</th>
                                </tr>
                                <tr>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th>Facebook</th>
                                    <th>Instagram</th>
                                    <th>Website</th>
                                </tr>
                            </thead>
                            <tbody id="token-list">
                                <?php
                                    include 'dbconnection.php';

                                    $search = isset($_GET['search']) ? $_GET['search'] : '';
                                    $status = isset($_GET['status']) ? $_GET['status'] : '';

                                    $sql = "SELECT * FROM airdrops_data";
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

                                    if (!empty($conditions)) {
                                        $sql .= " WHERE " . join(" AND ", $conditions);
                                    }

                                    $stmt = $conn->prepare($sql);

                                    if (!empty($params)) {
                                        $stmt->bind_param($types, ...$params);
                                    }

                                    $stmt->execute();
                                    $result = $stmt->get_result();

                                    $tokens = [];

                                    if ($result->num_rows > 0) {
                                        $index = 1;
                                        while ($row = $result->fetch_assoc()) {
                                            $crosses = 0;
                                            if (empty($row['Facebook'])) {
                                                $crosses++;
                                            }
                                            if (empty($row['Instagram'])) {
                                                $crosses++;
                                            }
                                            if (empty($row['Website'])) {
                                                $crosses++;
                                            }

                                            $tokens[] = [
                                                'id' => $row['id'],
                                                'airdrop_name' => $row['Title'],
                                                'Thumbnail' => $row['Thumbnail'],
                                                'Platform' => $row['Platform'],
                                                'RiskScore' => $row['RiskScore'],
                                                'Status' => $row['Status'],
                                                'Requirements' => $row['Requirements'],
                                                'Whitepaper' => $row['Whitepaper'],
                                                'Facebook' => $row['Facebook'],
                                                'Instagram' => $row['Instagram'],
                                                'Website' => $row['Website'],
                                                'TotalValue' => $row['TotalValue'],
                                                'crosses' => $crosses
                                            ];

                                            echo '<tr>';
                                            echo '<td>' . $index++ . '</td>';
                                            echo '<td><a href="upcoming_details.php?id=' . htmlspecialchars($row['id']) . '" class="airdrop-item-link"><img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="upcomingtoken-logo"> ' . htmlspecialchars($row['Title']) . '</a></td>';
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
                                            echo '<div class="custom-legend-color" style="background-color: #ffcd56;"></div>';
                                            echo 'Neutral: ' . htmlspecialchars($row['neutral_percentage']) . '%';
                                            echo '</div>';
                                            echo '<div class="custom-legend-item">';
                                            echo '<div class="custom-legend-color" style="background-color: #ff6384;"></div>';
                                            echo 'Negative: ' . htmlspecialchars($row['negative_percentage']) . '%';
                                            echo '</div>';
                                            echo '</div>';
                                            echo '</td>';

                                            $requirementStatus = htmlspecialchars($row['Requirements']);
                                            $requirementsymbol = ($requirementStatus != 'n/a') ? '✔' : '✘';
                                            echo '<td><span class="requirementsymbol">' . $requirementsymbol . '</span>' . '</td>';

                                            $whitepaperStatus = htmlspecialchars($row['Whitepaper']);
                                            $whitepaperClass = ($whitepaperStatus != 'n/a') ? '✔' : '✘';
                                            echo '<td><span class="whitepaperClass">' . $whitepaperClass . '</span>' . '</td>';

                                            $facebookStatus = htmlspecialchars($row['Facebook']);
                                            $facebookClass = ($facebookStatus != 'n/a') ? '✔' : '✘';
                                            echo '<td><span class="facebookClass">' . $facebookClass . '</span>' . '</td>';

                                            $instagramStatus = htmlspecialchars($row['Instagram']);
                                            $instagramClass = ($instagramStatus != 'n/a') ? '✔' : '✘';
                                            echo '<td><span class="instagramClass">' . $instagramClass . '</span>' . '</td>';

                                            $websiteStatus = htmlspecialchars($row['Website']);
                                            $websiteClass = ($websiteStatus != 'n/a') ? '✔' : '✘';
                                            echo '<td><span class="websiteClass">' . $websiteClass . '</span>' . '</td>';
                                            echo '</tr>';
                                        }
                                    } else {
                                        echo '<tr><td colspan="11">No upcoming airdrops found</td></tr>';
                                    }
                                    $stmt->close();
                                    $conn->close();
                                ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
        <script src="script.js"></script>
    </div>
    <script src="script.js"></script>
    <script>
        let sentimentData = [];
        let tokenData = <?php echo json_encode($tokens); ?>;

        // Function to fetch sentiment data from JSON file
        function fetchSentimentData() {
            return fetch('data/sentiment_results.json')
                .then(response => response.json())
                .then(data => sentimentData = data)
                .catch(error => console.error('Error fetching sentiment data:', error));
        }

        // Function to merge sentiment data and token data
        function mergeData() {
            return tokenData.map(token => {
                const sentiment = sentimentData.find(s => s.airdrop_name === token.airdrop_name);
                return {
                    ...token,
                    ...sentiment
                };
            });
        }

        // Function to filter and display tokens
        function filterTokens(filter) {
            // Remove active class from all buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(button => button.classList.remove('active'));

            // Add active class to the clicked button
            document.getElementById(filter).classList.add('active');

            // Get the token list container
            const tokenList = document.getElementById('token-list');
            tokenList.innerHTML = ''; // Clear current list

            // Filter and display tokens based on the filters
            const mergedData = mergeData();
            let filteredTokens;

            // Filter based on high negative sentiments, crosses and risk score (to be added later)
            if (filter === 'dangerous-threats') {
                filteredTokens = mergedData.filter(token =>
                    (token.negative_percentage > 40 || token.crosses >= 3) && token.crosses < 5
                );
            } else if (filter === 'most-scanned') {
                // Assuming other filters have different criteria, adjust as necessary
                filteredTokens = mergedData; // Default to showing all tokens for demonstration
            } else if (filter === 'requirements-need') {
                filteredTokens = mergedData.filter(token => token.Requirements !== 'n/a');
            } else {
                // Handle other filters or default case
                filteredTokens = mergedData;
            }

            filteredTokens.forEach((token, index) => {
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
                    <td><span class="requirementsymbol">${token.Requirements !== 'n/a' ? '✔' : '✘'}</span></td>
                    <td><span class="whitepaperClass">${token.Whitepaper !== 'n/a' ? '✔' : '✘'}</span></td>
                    <td><span class="facebookClass">${token.Facebook !== 'n/a' ? '✔' : '✘'}</span></td>
                    <td><span class="instagramClass">${token.Instagram !== 'n/a' ? '✔' : '✘'}</span></td>
                    <td><span class="websiteClass">${token.Website !== 'n/a' ? '✔' : '✘'}</span></td>
                `;
                tokenList.appendChild(row);
            });
        }

        // Fetch data on page load
        document.addEventListener('DOMContentLoaded', () => {
            fetchSentimentData()
                .then(() => filterTokens('most-scanned'));
        });
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
