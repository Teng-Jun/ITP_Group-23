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
        .img {
            justify-content: center;
        }
        .full-width-card {
            width: 100%;
        }
        .card {
            justify-content: center;
            align-items: center;
            margin-top: 2em;
        }
        .detail-logo {
            width: 100vw;
            height: 100vh;
        }
        .disabled {
            pointer-events: none;
            color: grey;
            text-decoration: none; /* Optional: Remove underline from disabled links */
        }
    </style>
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
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body"><img src="' . htmlspecialchars($row['Thumbnail']) . '" alt="Token Logo" class="detail-logo"></div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Airdrop Name:</strong> ' . $airdropName . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Platform:</strong> ' . htmlspecialchars($row['Platform']) . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Status:</strong> ' . htmlspecialchars($row['Status']) . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Features:</strong> ' . htmlspecialchars($row['Features']) . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';

                        $guide = htmlspecialchars($row['Guide']);
                        $guideItems = explode(',', $guide); // Split the string by commas

                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Guide:</strong></p>';
                        echo '<ul>';
                        foreach ($guideItems as $item) {
                            echo '<li>' . trim($item, " '") . '</li>'; // Trim any leading/trailing whitespace or single quotes
                        }
                        echo '</ul>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Total Value:</strong> ' . htmlspecialchars($row['Total_Value']) . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Requirements:</strong> ' . htmlspecialchars($row['Requirements']) . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p><strong>Number of Previous Drops:</strong> ' . htmlspecialchars($row['Num_Of_Prev_Drops']) . '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<p>';
                        echo !empty($row['Website']) && $row['Website'] !== 'n/a' ? 
                            '<a href="' . htmlspecialchars($row['Website']) . '" target="_blank"><i class="fas fa-globe"></i> Project Website </a>' : 
                            '<span class="disabled"><i class="fas fa-globe"></i> Project Website </span>';
                        echo '</p>';

                        echo '<p>';
                        echo !empty($row['Whitepaper']) && $row['Whitepaper'] !== 'n/a' ? 
                            '<a href="' . htmlspecialchars($row['Whitepaper']) . '" target="_blank"><i class="fas fa-file-alt"></i> Whitepaper </a>' : 
                            '<span class="disabled"><i class="fas fa-file-alt"></i> Whitepaper </span>';
                        echo '</p>';

                        echo '<p>';
                        echo !empty($row['Facebook']) && $row['Facebook'] !== 'n/a' ? 
                            '<a href="' . htmlspecialchars($row['Facebook']) . '" target="_blank"><i class="fab fa-facebook-f"></i> Facebook </a>' : 
                            '<span class="disabled"><i class="fab fa-facebook-f"></i> Facebook </span>';
                        echo '</p>';

                        echo '<p>';
                        echo !empty($row['Telegram Group']) && $row['Telegram Group'] !== 'n/a' ? 
                            '<a href="' . htmlspecialchars($row['Telegram Group']) . '" target="_blank"><i class="fab fa-telegram-plane"></i> Telegram Group </a>' : 
                            '<span class="disabled"><i class="fab fa-telegram-plane"></i> Telegram Group </span>';
                        echo '</p>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        
                        echo '<div class="row">';
                        echo '<div class="card full-width-card">';
                        echo '<div class="card-body">';
                        echo '<h3 style="text-align:center; margin-top: 20px;"><strong>Reddit Sentiment Analysis<strong></h3>';
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
    <script src="script.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const airdropName = <?php echo json_encode($airdropName); ?>;
            fetch('data/sentiment_results2.json')
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

                        const total = airdrop.positive + airdrop.neutral + airdrop.negative;
                        const positivePercentage = ((airdrop.positive / total) * 100).toFixed(2);
                        const neutralPercentage = ((airdrop.neutral / total) * 100).toFixed(2);
                        const negativePercentage = ((airdrop.negative / total) * 100).toFixed(2);

                        const ctx = document.getElementById('sentimentChart').getContext('2d');

                        if (chartContainer.chartInstance) {
                            chartContainer.chartInstance.destroy();
                        }

                        chartContainer.chartInstance = new Chart(ctx, {
                            type: 'pie',
                            data: {
                                labels: ['Positive', 'Neutral', 'Negative'],
                                datasets: [{
                                    data: [positivePercentage, neutralPercentage, negativePercentage],
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
                        updateCustomLegend(chartContainer.chartInstance, legendContainer, positivePercentage, neutralPercentage, negativePercentage);

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

        function updateCustomLegend(chart, legendContainer, positive, neutral, negative) {
            legendContainer.innerHTML = `
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #36a2eb;"></div>
                    Positive: ${positive}%
                </div>
                <div class="custom-legend-item">
                    <div class="custom-legend-color" style="background-color: #ffcd56;"></div>
                    Neutral: ${neutral}%
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
