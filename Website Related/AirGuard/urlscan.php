<?php
require __DIR__.'/vendor/autoload.php';
// Load the .env file
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();
// Access VirusTotal API key from the .env file
$apiKey = $_ENV['VT_API_KEY'];
// Initialize variables for the form handling and the result
$scanResult = '';
$error = '';
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['url'])) {
    $urlToScan = trim($_POST['url']);
    // If URL doesn't start with 'http://' or 'https://', prepend 'https://'
    if (!preg_match("~^(?:f|ht)tps?://~i", $urlToScan)) {
        $urlToScan = "https://" . $urlToScan;
    }
    // Base64 encode the URL
    $encodedUrl = rtrim(strtr(base64_encode($urlToScan), '+/', '-_'), '=');
    // VirusTotal API URL for URL report (v3)
    $apiUrl = "https://www.virustotal.com/api/v3/urls/{$encodedUrl}";
    // Set up the headers for the GET request
    $options = array(
        'http' => array(
            'header' => "x-apikey: $apiKey\r\n" .
                        "accept: application/json\r\n",
            'method'  => 'GET',
        ),
    );
    // Create the context for the request
    $context  = stream_context_create($options);
    // Send the request to VirusTotal v3 API
    $result = @file_get_contents($apiUrl, false, $context);
    // Handle errors
    if ($result === FALSE) {
        $error = 'Error occurred while connecting to VirusTotal. Please try again later.';
    } else {
        // Decode and display the response
        $response = json_decode($result, true);
        if (isset($response['data'])) {
            // Parse response to make it more readable
            $scanResult = '<div class="row"><div class="col-md-6"><h3>URL Analysis Report</h3>';
            $scanResult .= '<p><strong>URL Scanned:</strong> ' . htmlspecialchars($urlToScan) . '</p>';
            $scanResult .= '<p><strong>Analysis ID:</strong> ' . htmlspecialchars($response['data']['id']) . '</p>';
            $scanResult .= '<p><strong>Date Scanned:</strong> ' . date('Y-m-d H:i:s', $response['data']['attributes']['last_analysis_date']) . '</p>';
            // Initialize categories
            $clean = [];
            $unrated = [];
            $malicious = [];
            foreach ($response['data']['attributes']['last_analysis_results'] as $engine => $result) {
                switch ($result['category']) {
                    case 'harmless':
                        $clean[] = $engine;
                        break;
                    case 'undetected':
                    case 'unrated':
                        $unrated[] = $engine;
                        break;
                    default:
                        $malicious[] = $engine;
                        break;
                }
            }
            // Display results
            $scanResult .= '<h4>Clean Engines</h4><ul>';
            foreach ($clean as $engine) {
                $scanResult .= "<li class='clean'><strong>$engine:</strong> Clean</li>";
            }
            $scanResult .= '</ul>';
            $scanResult .= '<h4>Unrated/Undetected Engines</h4><ul>';
            foreach ($unrated as $engine) {
                $scanResult .= "<li class='unrated'><strong>$engine:</strong> Unrated/Undetected</li>";
            }
            $scanResult .= '</ul>';
            $scanResult .= '<h4>Potentially Malicious Engines</h4><ul>';
            foreach ($malicious as $engine) {
                $scanResult .= "<li class='malicious'><strong>$engine:</strong> Malicious</li>";
            }
            $scanResult .= '</ul></div>';
            // Add Pie Chart next to the results
            $scanResult .= '<div class="col-md-6">
                                <h4>Scan Result Breakdown</h4>
                                <canvas id="resultChart" width="300" height="300"></canvas>
                            </div></div>';
        } else {
            $error = 'Failed to retrieve URL analysis report.';
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scan URL - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .clean { color: green; }
        .unrated { color: orange; }
        .malicious { color: red; }
    </style>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="mx-auto my-5" style="max-width: 1050px;">
        <h2>Scan a URL for Threats</h2>
        <p style="font-weight: bold; color: red;">
        These URL scanners utilize the VirusTotal API. However, it is strongly advised that users should also perform
        their own due diligence and not rely solely on the results provided.
        </p>        
        <form action="urlscan.php" method="POST">
            <div class="form-group">
                <label for="url">Enter URL to Scan:</label>
                <input type="text" class="form-control" name="url" id="url" placeholder="example.com" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>

        <?php if ($error): ?>
            <div class="alert alert-danger mt-4" role="alert">
                <?php echo $error; ?>
            </div>
        <?php elseif ($scanResult): ?>
            <div class="alert alert-success mt-4" role="alert">
                <?php echo $scanResult; ?>
            </div>

            <!-- Add Pie Chart -->
            <script>
                var ctx = document.getElementById('resultChart').getContext('2d');
                var resultChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ['Clean', 'Unrated/Undetected', 'Malicious'],
                        datasets: [{
                            label: 'Analysis Results',
                            data: [<?php echo count($clean); ?>, <?php echo count($unrated); ?>, <?php echo count($malicious); ?>],
                            backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
                        }]
                    },
                    options: {
                        responsive: true
                    }
                });
            </script>
        <?php endif; ?>
    </div>
</body>
</html>
