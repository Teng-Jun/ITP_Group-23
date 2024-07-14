<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upcoming Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
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

                $sql = "SELECT id, tle, Platform, Status, Thumbnail FROM airdrops_data_speculative";
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
                        echo '<a href="upcoming_details.php?id=' . htmlspecialchars($row['id']) . '" class="airdrop-item-link">';
                        echo '<img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="airdrop-logo">';
                        echo '<div class="airdrop-info">';
                        echo '<h3>' . htmlspecialchars($row['tle']) . '</h3>';
                        echo '<p>Platform: ' . htmlspecialchars($row['Platform']) . '</p>';
                        echo '<p>Status: <span class="' . ($row['Status'] == 'Airdrop Confirmed' ? 'status-confirmed' : ($row['Status'] == 'Airdrop Unconfirmed' ? 'status-pending' : 'status-expired')) . '">' . htmlspecialchars($row['Status']) . '</span></p>';
                        echo '</a>'; // Closing the anchor tag here
                        echo '<button type="button" onclick="showChart(\'' . htmlspecialchars($row['tle']) . '\', this)">Show Sentiment</button>';
                        echo '<div class="chart-container" style="display:none;"><canvas></canvas></div>';
                        echo '<div class="no-data" style="display:none;">No data from Reddit forum.</div>';
                        echo '<div class="custom-legend" style="display:none;"></div>'; // Updated custom legend for showing the numbers
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
                })
                .catch(error => {
                    console.error('Error fetching sentiment data:', error);
                    alert('Failed to load sentiment data.');
                });
        }
    </script>
</body>
</html>
