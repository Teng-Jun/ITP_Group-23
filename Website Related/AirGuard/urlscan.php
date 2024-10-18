<?php
require_once 'vendor/autoload.php';

// Load .env variables
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();
$apiKey = $_ENV['URLSCAN_API_KEY']; // Ensure this matches your .env file exactly

function submitUrlScan($url, $apiKey) {
    $data = json_encode(array("url" => $url));
    $ch = curl_init('https://urlscan.io/api/v1/scan/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json',
        'API-Key: ' . $apiKey
    ));
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

function retrieveScanResults($uuid, $apiKey) {
    $ch = curl_init('https://urlscan.io/api/v1/result/' . $uuid . '/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('API-Key: ' . $apiKey));

    // Attempt to fetch results with retries
    for ($attempts = 0; $attempts < 5; $attempts++) {
        sleep(10);  // Wait for 10 seconds before each attempt
        $response = curl_exec($ch);
        $result = json_decode($response, true);
        if (!isset($result['message']) || $result['message'] !== 'Scan is not finished yet') {
            curl_close($ch);
            return $result;
        }
    }
    curl_close($ch);
    return null;  // Return null if scan isn't ready
}

$results = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['url'])) {
    $urlToScan = $_POST['url'];
    $scanResult = submitUrlScan($urlToScan, $apiKey);

    if (isset($scanResult['uuid'])) {
        $uuid = $scanResult['uuid'];
        $results = retrieveScanResults($uuid, $apiKey);

        if ($results === null) {
            $error = "Failed to retrieve scan results. Please try again.";
        } else {
            // Convert scan time to local time
            $scanTimeUTC = $results['task']['time'] ?? 'N/A';
            if ($scanTimeUTC !== 'N/A') {
                $date = new DateTime($scanTimeUTC, new DateTimeZone('UTC'));
                $date->setTimezone(new DateTimeZone('Asia/Singapore'));  // Adjust to your timezone
                $localScanTime = $date->format('Y-m-d H:i:s');
            } else {
                $localScanTime = 'N/A';
            }

            // Capitalize country name
            $brandCountry = strtoupper($results['verdicts']['urlscan']['brands'][0]['country'][0] ?? 'N/A');
        }
    } else {
        $error = "Failed to submit the scan. Please check the URL and try again.";
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .clean { color: green; }
        .unrated { color: orange; }
        .progress-message { color: blue; font-weight: bold; }
        .malicious { color: red; }
    </style>
    <script>
        function showProgressMessage() {
            document.getElementById('progressMessage').style.display = 'block';
        }
        function showErrorMessage(errorMessage) {
            if (errorMessage) {
                alert(errorMessage);
            }
        }
    </script>
</head>
<body>
    <body onload="showErrorMessage('<?= $error ?? '' ?>')">
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="container my-5">
        <h2>Scan a URL for Threats</h2>
        <form id="apiForm" method="POST" onsubmit="showProgressMessage()">
            <div class="form-row">
                <div class="form-group col-md-6">
                    <label for="api">Choose API:</label>
                    <select id="api" name="api" class="form-control" required>
                        <option value="urlscanio">urlscan.io</option>
                    </select>
                </div>
                <div class="form-group col-md-6">
                    <label for="url">Enter URL to Scan:</label>
                    <input type="text" class="form-control" name="url" id="url" placeholder="example.com" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <!-- Progress Message -->
        <div id="progressMessage" class="progress-message mt-4" style="display: none;">
            Scanning in progress. Please wait...
        </div>
        <div id="result" class="mt-4">
            <?php if (isset($results)): ?>
                <h3>Scan Results</h3>
                <div class="row">
                    <!-- General Information -->
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">General Information</div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">URL: <?= htmlspecialchars($results['page']['url']); ?></li>
                                <li class="list-group-item">IP Address: <?= htmlspecialchars($results['page']['ip'] ?? 'N/A'); ?></li>
                                <li class="list-group-item">ASN: <?= htmlspecialchars($results['page']['asn'] ?? 'N/A'); ?></li>
                                <li class="list-group-item">Scan Time: <?= htmlspecialchars($localScanTime); ?></li>
                            </ul>
                        </div>
                    </div>

                    <!-- Security Threats -->
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Security Threats</div>
                            <ul class="list-group list-group-flush">
                                <?php if (!empty($results['verdicts']['overall']['malicious'])): ?>
                                    <li class="list-group-item malicious">This URL is Malicious</li>
                                <?php else: ?>
                                    <li class="list-group-item clean">This URL is most likely clean</li>
                                <?php endif; ?>

                                <li class="list-group-item">
                                    <strong>Score:</strong> <?= htmlspecialchars($results['verdicts']['urlscan']['score'] ?? 'N/A'); ?>
                                </li>
                                <li class="list-group-item">
                                    <strong>Categories:</strong> 
                                    <?= !empty($results['verdicts']['urlscan']['categories']) 
                                        ? implode(', ', $results['verdicts']['urlscan']['categories']) 
                                        : 'N/A'; ?>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="row mt-4">
                    <!-- Brand Detection -->
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Brand Detection</div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">
                                    <strong>Brand:</strong> <?= htmlspecialchars($results['verdicts']['urlscan']['brands'][0]['name'] ?? 'None'); ?>
                                </li>
                                <li class="list-group-item">
                                    <strong>Country:</strong> <?= htmlspecialchars($brandCountry); ?>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!-- Network and Redirect Information -->
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Network & Redirect Info</div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">
                                    <strong>Redirected:</strong> <?= $results['page']['redirected'] ? 'Yes' : 'No'; ?>
                                </li>
                                <li class="list-group-item">
                                    <strong>Server:</strong> <?= htmlspecialchars($results['page']['server'] ?? 'N/A'); ?>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="row mt-4">
                    <!-- Contacted Domains -->
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">Contacted Domains</div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">
                                    <?= !empty($results['lists']['domains']) 
                                        ? implode(', ', $results['lists']['domains']) 
                                        : 'No Domains Contacted'; ?>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
