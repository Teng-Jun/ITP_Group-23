<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Details - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels"></script>
    <style>
        .chart-container {
            width: 300px;
            height: 300px;
            margin: 0 auto; 
        }
        .no-data {
            color: red;
            font-weight: bold;
            text-align: center;  
        }
        .custom-legend {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        .custom-legend-item {
            display: flex;
            align-items: center;
            margin-right: 20px;  
            font-size: 16px;  
        }
        .custom-legend-color {
            width: 20px;  
            height: 20px;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper">
        <main>
            <a href="upcoming.php" class="back-button">Back to Upcoming Airdrops</a>
            <h2>Airdrop Details</h2>
            <div class="container">
            <div class="airdrop-details">
                <?php
                include 'dbconnection.php';

                $id = isset($_GET['id']) ? $_GET['id'] : '';
                $sql = "SELECT * FROM airdrops_data_speculative WHERE id = ?";

                $stmt = $conn->prepare($sql);
                $stmt->bind_param("i", $id); // Assuming 'id' is an integer
                $stmt->execute();
                $result = $stmt->get_result();

                if ($result->num_rows > 0) {
                    $row = $result->fetch_assoc();
                    $airdropName = htmlspecialchars($row['tle']);
                    echo '<div class="detail-item">';
                    echo '<img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="detail-logo">';
                    echo '<h3>' . $airdropName . '</h3>';
                    echo '<p>Platform: ' . htmlspecialchars($row['Platform']) . '</p>';
                    echo '<p>Status: ' . htmlspecialchars($row['Status']) . '</p>';
                    echo '<p>Features: ' . htmlspecialchars($row['Features']) . '</p>';
                    $guide = htmlspecialchars($row['Guide']);
                    $guide = str_replace(['[', ']'], '', $guide); // Removes square brackets
                    echo '<p>Guide: ' . $guide . '</p>';
                    echo '<p>Total Value: ' . htmlspecialchars($row['Total_Value']) . '</p>';
                    echo '<p>Requirements: ' . htmlspecialchars($row['Requirements']) . '</p>';
                    echo '<p>Number of Previous Drops: ' . htmlspecialchars($row['Num_Of_Prev_Drops']) . '</p>';
                    echo '<p><a href="' . htmlspecialchars($row['Website']) . '">Project Website</a></p>';
                    echo '<p><a href="' . htmlspecialchars($row['Whitepaper']) . '">Whitepaper</a></p>';
                    echo '<p>Facebook: ' . htmlspecialchars($row['Facebook']) . '</p>';
                    echo '<p>Telegram Group: ' . htmlspecialchars($row['Telegram Group']) . '</p>';
                    echo '</div>';
                    echo '<h3 style="text-align:center; margin-top: 20px;">Reddit Sentiment Analysis</h3>';
                    echo '<div class="chart-container"><canvas id="sentimentChart"></canvas></div>';
                    echo '<div class="no-data" style="display:none;">No data from Reddit forum.</div>';
                    echo '<div class="custom-legend" style="display:none;"></div>';
                } else {
                    echo "Airdrop details not found.";
                }
                $stmt->close();
                $conn->close();
                ?>
            </div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const airdropName = <?php echo json_encode($airdropName); ?>;
            fetch('data/sentiment_results.json') 
                .then(response => response.json())
                .then(data => {
                    const airdrop = data.find(item => item.airdrop_name === airdropName);
                    const chartContainer = document.querySelector('.chart-container');
                    const noDataContainer = document.querySelector('.no-data');
                    const legendContainer = document.querySelector('.custom-legend');

                    if (airdrop && (airdrop.positive > 0 || airdrop.neutral > 0 || airdrop.negative > 0)) {
                        chartContainer.style.display = 'block';
                        noDataContainer.style.display = 'none';
                        legendContainer.style.display = 'flex';
                        const ctx = document.getElementById('sentimentChart').getContext('2d');

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
                                            return value; // Show the value directly on the chart
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
                                events: ['mousemove'] 
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
        });

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
    </script>
</body>
</html>
