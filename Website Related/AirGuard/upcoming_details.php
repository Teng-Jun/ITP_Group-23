<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Details - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels"></script>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper">
        <main>
            <button onclick="history.back()" class="btn btn-primary back-button">Back</button>
            <h2>Airdrop Details</h2>
            <div class="container">
                <div class="airdrop-details">
                    <?php
                    include 'dbconnection.php';

                    $id = isset($_GET['id']) ? $_GET['id'] : '';
                    $sql = "SELECT * FROM airdrops_data WHERE id = ?";

                    $stmt = $conn->prepare($sql);
                    $stmt->bind_param("i", $id); // Assuming 'id' is an integer
                    $stmt->execute();
                    $result = $stmt->get_result();

                    if ($result->num_rows > 0) {
                        $row = $result->fetch_assoc();
                        $airdropName = htmlspecialchars($row['Title']);
                       
                        echo '<div class="row1">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body d-flex align-items-center">';
                        echo '<div class="col-md-3"><img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="detail-logo"></div>';
                        echo '<div class="col-md-9"><p><strong>Features:</strong> ' . htmlspecialchars($row['Features']) . '</p></div>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';

                        echo '<div class="overview-section">';
                        echo '<h3>Overview</h3>';
                        echo '<div class="row">';
                        echo '<div class="col-md-6">';
                        echo '<p><i class="fas fa-globe"></i> Website: ' . ($row['Website'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Website']) . '" target="_blank"><i class="fas fa-globe"></i></a>' : 'n/a') . '</p>';
                        echo '<p><i class="fas fa-tags"></i> Ticker: ' . htmlspecialchars($row['Ticker']) . '</p>';
                        echo '<p><i class="fas fa-database"></i> Total Supply: ' . htmlspecialchars($row['Total_Supply']) . '</p>';
                        echo '<p><i class="fas fa-file-alt"></i> Whitepaper: ' . ($row['Whitepaper'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Whitepaper']) . '" target="_blank">Download Whitepaper</a>' : 'n/a') . '</p>';
                        echo '<p><i class="fab fa-twitter"></i> Twitter: ' . ($row['Twitter'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Twitter']) . '" target="_blank"><i class="fab fa-twitter"></i></a>' : 'n/a') . '</p>';
                        echo '<p><i class="fab fa-facebook"></i> Facebook: ' . ($row['Facebook'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Facebook']) . '" target="_blank"><i class="fab fa-facebook"></i></a>' : 'n/a') . '</p>';
                        echo '</div>';
                        echo '<div class="col-md-6">';
                        echo '<p><i class="fas fa-paper-plane"></i> Telegram Group: ' . ($row['Telegram Group'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Telegram Group']) . '" target="_blank"><i class="fas fa-paper-plane"></i></a>' : 'n/a') . '</p>';
                        echo '<p><i class="fas fa-paper-plane"></i> Telegram Channel: ' . ($row['Telegram Channel'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Telegram Channel']) . '" target="_blank"><i class="fas fa-paper-plane"></i></a>' : 'n/a') . '</p>';
                        echo '<p><i class="fab fa-discord"></i> Discord Chat: ' . ($row['Discord'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Discord']) . '" target="_blank"><i class="fab fa-discord"></i></a>' : 'n/a') . '</p>';
                        echo '<p><i class="fab fa-medium"></i> Blog: ' . ($row['Medium'] != 'n/a' ? '<a href="' . htmlspecialchars($row['Medium']) . '" target="_blank"><i class="fab fa-medium"></i></a>' : 'n/a') . '</p>';
                        echo '<p><i class="fab fa-github"></i> GitHub Repository: ' . ($row['GitHub'] != 'n/a' ? '<a href="' . htmlspecialchars($row['GitHub']) . '" target="_blank"><i class="fab fa-github"></i></a>' : 'n/a') . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';

                        echo '<div class="metrics-box">';
                        echo '<div><strong>Total Value</strong><p>' . htmlspecialchars($row['Total_Value']) . '</p></div>';
                        echo '<div><strong>Requirements</strong><p>' . htmlspecialchars($row['Requirements']) . '</p></div>';
                        echo '<div><strong>Number of Previous Drops</strong><p>' . htmlspecialchars($row['Num_Of_Prev_Drops']) . '</p></div>';
                        echo '<div><strong>Temperature</strong><p>' . htmlspecialchars($row['Temp']) . '</p></div>';
                        echo '</div>';

                        $guide = htmlspecialchars($row['Guide']);
                        $guide = trim($guide, "[]'"); // Remove the square brackets and single quotes

                        // Split the guide text by period followed by a single quote and then a space to ensure sentences are kept together
                        $guideItems = preg_split("/(?<=\.)'/", $guide);

                        echo '<div class="row3">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Guide:</strong></p>';
                        echo '<div>'; // Change to div to remove bullet points
                        foreach ($guideItems as $item) {
                            $cleanedItem = trim($item, "' ,"); // Remove leading/trailing single quote, comma and whitespace
                            echo '<p>' . trim($cleanedItem) . '</p>'; // Trim any leading/trailing whitespace and change to paragraph
                        }
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';

                        echo '<div class="row4">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<h3 style="text-align:center; margin-top: 20px;"><strong>Reddit Sentiment Analysis</strong></h3>';
                        echo '<div class="chart-container"><canvas id="sentimentChart"></canvas></div>';
                        echo '<div class="no-data" style="display:none;">No data from Reddit forum.</div>';
                        echo '<div class="custom-legend" style="display:none;"></div>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';

                    } else {
                        echo "Airdrop details not found.";
                    }
                    $stmt->close();
                    $conn->close();
                    ?>
                </div>
            </div>
        </main>
        <script src="script.js"></script>
    </div>
         <!-- Add the footer include here -->
         <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>
    <script src="script.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const airdropName = <?php echo json_encode($airdropName); ?>;
            fetch('data/sentiment_results_20241118_003834.json')
                .then(response => response.json())
                .then(data => {
                    const airdrop = data.find(item => item.airdrop_name === airdropName);
                    const chartContainer = document.querySelector('.chart-container');
                    const noDataContainer = document.querySelector('.no-data');
                    const legendContainer = document.querySelector('.custom-legend');

                    if (airdrop && (airdrop.positive > 0 || airdrop.negative > 0)) {
                        chartContainer.style.display = 'block';
                        noDataContainer.style.display = 'none';
                        legendContainer.style.display = 'flex';

                        const total = airdrop.positive + airdrop.negative;
                        const positivePercentage = ((airdrop.positive / total) * 100).toFixed(2);
                        const negativePercentage = ((airdrop.negative / total) * 100).toFixed(2);

                        const ctx = document.getElementById('sentimentChart').getContext('2d');

                        if (chartContainer.chartInstance) {
                            chartContainer.chartInstance.destroy();
                        }

                        chartContainer.chartInstance = new Chart(ctx, {
                            type: 'pie',
                            data: {
                                labels: ['Positive', 'Negative'],
                                datasets: [{
                                    data: [positivePercentage, negativePercentage],
                                    backgroundColor: ['#36a2eb', '#ff6384']
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
                                            return value + '%'; // Show the value directly on the chart, rounded to 2 decimal places
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
                        updateCustomLegend(chartContainer.chartInstance, legendContainer, positivePercentage, negativePercentage);

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

        function updateCustomLegend(chart, legendContainer, positive, negative) {
            legendContainer.innerHTML = `
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #36a2eb;"></div>
                    Positive: ${positive}%
                </div>
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #ff6384;"></div>
                    Negative: ${negative}%
                </div>
            `;
        }
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
