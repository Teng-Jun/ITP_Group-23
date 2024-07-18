<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upcoming Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels"></script>
    <style>
        .chart-container {
            width: 300px;  
            height: 300px; 
        }
        .no-data {
            color: red;
            font-weight: bold;
        }
        .custom-legend {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        .custom-legend-item {
            display: flex;
            align-items: center;
            margin-right: 10px;
        }
        .custom-legend-color {
            width: 12px;
            height: 12px;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header-container">
            <?php include 'header.php'; ?>
        </div>
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
                    <button type="submit">Search</button>
                    <button type="button" id="resetButton">Reset</button>
                </form>
            </section>
            <div class="tabs">
                <button class="tab-button active">Tokens: Most Scanned</button>
                <button class="tab-button">Tokens: Dangerous Threats</button>
                <button class="tab-button">Tokens: by Market Cap</button>
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
                                <th>Sentiments</th>
                                <th>Requirements</th>
                                <th>Whitepaper</th>
                                <th>Social</th>
                                <th>Media</th>
                                <th></th>
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
                        <tbody>
                            <?php
                                include 'dbconnection.php';

                                $search = isset($_GET['search']) ? $_GET['search'] : '';
                                $status = isset($_GET['status']) ? $_GET['status'] : '';

                                $sql = "SELECT * FROM airdrops_data_speculative";
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
                                    $index = 1;
                                    while($row = $result->fetch_assoc()) {
                                        echo '<tr>';
                                        echo '<td>' . $index++ . '</td>';
                                        echo '<td><a href="upcoming_details.php?id=' . htmlspecialchars($row['id']) . '" class="airdrop-item-link"><img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="token-logo"> ' . htmlspecialchars($row['tle']) . '</a></td>';
                                        echo '<td>' . htmlspecialchars($row['Platform']) . '</td>';
                                        echo '<td>' . htmlspecialchars($row['RiskScore']) . '</td>';
                                        echo '<td class="' . ($row['Status'] == 'Airdrop Confirmed' ? 'status-confirmed' : ($row['Status'] == 'Airdrop Unconfirmed' ? 'status-pending' : 'status-expired')) . '">' . htmlspecialchars($row['Status']) . '</td>';
                                        echo '<td><button type="button" class="btn" onclick="showChart(\'' . htmlspecialchars($row['tle']) . '\', this)">Show Sentiment</button>';
                                        echo '<div class="chart-container" style="display:none;"><canvas></canvas></div>';
                                        echo '<div class="no-data" style="display:none;">No data from Reddit forum.</div>';
                                        echo '<div class="custom-legend" style="display:none;"></div>';
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
                                        echo '<tr><td colspan="7">No upcoming airdrops found</td></tr>';
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
    </div>
    <script src="script.js"></script>
    <script>
        function updateCustomLegend(chart, legendContainer) {
            const data = chart.data.datasets[0].data;
            legendContainer.innerHTML = `
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #36a2eb;"></div>
                    Positive: ${data[0]}
                </div>
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #ffcd56;"></div>
                    Neutral: ${data[1]}
                </div>
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #ff6384;"></div>
                    Negative: ${data[2]}
                </div>
            `;
        }

        function showChart(airdropName, button) {
        fetch('data/sentiment_results.json')
            .then(response => response.json())
            .then(data => {
                const airdrop = data.find(item => item.airdrop_name === airdropName);
                const chartContainer = button.nextElementSibling;
                const noDataContainer = chartContainer.nextElementSibling;
                const legendContainer = noDataContainer.nextElementSibling;

                if (chartContainer.style.display === 'none' || chartContainer.style.display === '') {
                    if (airdrop && (airdrop.positive > 0 || airdrop.neutral > 0 || airdrop.negative > 0)) {
                        chartContainer.style.display = 'block';
                        noDataContainer.style.display = 'none';
                        legendContainer.style.display = 'flex';
                        const ctx = chartContainer.querySelector('canvas').getContext('2d');

                        if (chartContainer.chartInstance) {
                            chartContainer.chartInstance.destroy();
                        }

                        chartContainer.chartInstance = new Chart(ctx, {
                            type: 'pie',
                            data: {
                                labels: ['Positive', 'Neutral', 'Negative'],
                                datasets: [{
                                    data: [airdrop.positive, airdrop.neutral, airdrop.negative],
                                    backgroundColor: ['#36a2eb', '#ffcd56', '#ff6384']
                                }]
                            },
                            options: {
                                responsive: true,
                                title: {
                                    display: true,
                                    text: `Sentiment Distribution for ${airdropName}`
                                },
                                plugins: {
                                    datalabels: {
                                        formatter: (value, context) => {
                                            return value;
                                        },
                                        color: '#fff',
                                        font: {
                                            weight: 'bold'
                                        }
                                    }
                                },
                                legend: {
                                    display: true
                                },
                                onClick: function(e, legendItem) {
                                    const chart = this;
                                    const index = legendItem[0].index;
                                    chart.getDatasetMeta(0).data[index].hidden = !chart.getDatasetMeta(0).data[index].hidden;
                                    chart.update();
                                    updateCustomLegend(chart, legendContainer);
                                }
                            }
                        });

                        // Custom legend
                        updateCustomLegend(chartContainer.chartInstance, legendContainer);

                    } else {
                        chartContainer.style.display = 'none';
                        noDataContainer.style.display = 'block';
                        legendContainer.style.display = 'none';
                    }
                } else {
                    chartContainer.style.display = 'none';
                    noDataContainer.style.display = 'none';
                    legendContainer.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error fetching sentiment data:', error);
                alert('Failed to load sentiment data.');
            });
        }
    </script>
</body>
</html>
