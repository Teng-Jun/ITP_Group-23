<?php
require_once 'vendor/autoload.php';

// Load .env variables
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();

$apiKey = $_ENV['CP_API_KEY'];
if (!$apiKey) {
    die("API key not found.");
}

$statusResult = null; // Variable to hold the scan results

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url'])) {
    $urlToScan = filter_var($_POST['url'], FILTER_SANITIZE_URL);
    $scanResult = initiateScan($urlToScan);

    if ($scanResult && isset($scanResult['jobID'])) {
        $jobID = $scanResult['jobID'];
        $statusResult = pollScanStatus($jobID);
    } else {
        echo "<p>Failed to initiate the scan or jobID not found.</p>";
    }
}

// Function to initiate the scan
function initiateScan($url) {
    global $apiKey;
    $apiEndpoint = "https://developers.checkphish.ai/api/neo/scan";
    $postData = json_encode([
        "apiKey" => $apiKey,
        "urlInfo" => ["url" => $url],
        "scanType" => "full"
    ]);
    return sendCurlRequest($apiEndpoint, $postData);
}

// Function to poll the scan status until it's complete
function pollScanStatus($jobID) {
    while (true) {
        $statusResult = getScanStatus($jobID);
        if ($statusResult) {
            if ($statusResult['status'] === 'DONE') {
                return $statusResult;
            } else {
                sleep(5);
            }
        } else {
            echo "<p>Failed to retrieve scan status.</p>";
            break;
        }
    }
    return null;
}

// Function to get the scan status
function getScanStatus($jobID) {
    global $apiKey;
    $apiEndpoint = "https://developers.checkphish.ai/api/neo/scan/status";
    $postData = json_encode([
        "apiKey" => $apiKey,
        "jobID" => $jobID,
        "insights" => true
    ]);
    return sendCurlRequest($apiEndpoint, $postData);
}

// Helper function to send cURL requests
function sendCurlRequest($url, $data) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Scanner</title>
</head>
<body>
    <h1>Scan a URL</h1>
    <form method="POST">
        <label for="url">Enter a URL:</label>
        <input type="url" name="url" id="url" required>
        <button type="submit">Scan</button>
    </form>

    <?php if ($statusResult): ?>
        <h2>Scan Results</h2>
        <p><strong>Job ID:</strong> <?= htmlspecialchars($statusResult['job_id']) ?></p>
        <p><strong>Status:</strong> <?= htmlspecialchars($statusResult['status']) ?></p>
        <p><strong>URL:</strong> <?= htmlspecialchars($statusResult['url']) ?></p>
        <p><strong>SHA256:</strong> <?= htmlspecialchars($statusResult['url_sha256']) ?></p>
        <p><strong>Disposition:</strong> <?= htmlspecialchars($statusResult['disposition']) ?></p>
        <p><strong>Brand:</strong> <?= htmlspecialchars($statusResult['brand'] ?? 'N/A') ?></p>
        <p><strong>Resolved:</strong> <?= $statusResult['resolved'] ? 'Yes' : 'No' ?></p>
        <p><strong>Insights Link:</strong> <a href="<?= htmlspecialchars($statusResult['insights']) ?>" target="_blank">View Insights</a></p>
        <?php if (isset($statusResult['screenshot_path'])): ?>
            <p><strong>Screenshot:</strong></p>
            <img src="<?= htmlspecialchars($statusResult['screenshot_path']) ?>" alt="Screenshot" width="600">
            <br><a href="<?= htmlspecialchars($statusResult['screenshot_path']) ?>" download>Download Screenshot</a>
        <?php else: ?>
            <p>No screenshot available.</p>
        <?php endif; ?>
        <p><strong>Scan Start:</strong> <?= date('Y-m-d H:i:s', $statusResult['scan_start_ts'] / 1000) ?></p>
        <p><strong>Scan End:</strong> <?= date('Y-m-d H:i:s', $statusResult['scan_end_ts'] / 1000) ?></p>
    <?php endif; ?>
</body>
</html>
