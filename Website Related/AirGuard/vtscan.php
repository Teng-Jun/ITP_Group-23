<?php
require_once 'vendor/autoload.php';

// Load .env variables
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();
$apiKey = $_ENV['VT_API_KEY'];

function submitUrlToVirusTotal($url, $apiKey) {
    $curlHandle = curl_init('https://www.virustotal.com/api/v3/urls');
    curl_setopt_array($curlHandle, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => http_build_query(["url" => $url]),
        CURLOPT_HTTPHEADER     => ['x-apikey: ' . $apiKey]
    ]);
    $response = curl_exec($curlHandle);
    curl_close($curlHandle);
    $responseArray = json_decode($response, true);
    return $responseArray['data']['id'] ?? null;
}

function retrieveVirusTotalResults($id, $apiKey) {
    $curlHandle = curl_init('https://www.virustotal.com/api/v3/analyses/' . $id);
    curl_setopt_array($curlHandle, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => ['x-apikey: ' . $apiKey]
    ]);
    $response = curl_exec($curlHandle);
    curl_close($curlHandle);
    return json_decode($response, true);
}

$results = null;
$error = null;
$urlToScan = null;
$scanInitiatedAt = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url'])) {
    $urlToScan = $_POST['url'];
    $scanInitiatedAt = date('Y-m-d H:i:s'); // Capture the time when the scan was initiated
    $itemId = submitUrlToVirusTotal($urlToScan, $apiKey);

    if ($itemId) {
        sleep(5); // Wait for VirusTotal analysis to complete
        $results = retrieveVirusTotalResults($itemId, $apiKey);
    } else {
        $error = "Failed to submit the URL for scanning. Please verify the URL and try again.";
    }
}

include 'header.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scan URL - AirGuard</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 1200px; margin: auto; padding-top: 20px; }
        .card { background: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 5px; margin-top: 20px; }
        .result-item { margin-bottom: 10px; }
        .result-header { font-size: 18px; font-weight: bold; margin-bottom: 15px; }
        .result-value { font-size: 16px; }
        .clean, .harmless { color: green; }
        .malicious, .suspicious { color: red; }
        .undetected { color: gray; }
        .progress-message { color: blue; font-weight: bold; display: none; margin-top: 20px; }
        table { width: 100%; margin-top: 20px; }
        th, td { text-align: left; padding: 8px; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body onload="showErrorMessage('<?= $error ?? '' ?>')">
    <div class="container">
        <h2>Scan a URL for Threats</h2>
        <form id="apiForm" method="POST" onsubmit="showProgressMessage()">
            <div class="form-row">
                <div class="col-md-4">
                    <label for="api">Choose API:</label>
                    <select id="api" name="api" class="form-control" required>
                        <option value="virustotal">VirusTotal</option>
                    </select>
                </div>
                <div class="col-md-8">
                    <label for="url">Enter URL to Scan:</label>
                    <input type="text" class="form-control" name="url" id="url" placeholder="http://example.com" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <div id="progressMessage" class="progress-message">Scanning in progress. Please wait...</div>
        <?php if ($urlToScan && $scanInitiatedAt): ?>
            <div class="card">
                <div class="result-header">Scan Details</div>
                <table>
                    <tr><th>Scanned URL</th><td><?= htmlspecialchars($urlToScan) ?></td></tr>
                    <tr><th>Scan initiated at</th><td><?= $scanInitiatedAt ?></td></tr>
                </table>
            </div>
        <?php endif; ?>
        <?php if (isset($results) && isset($results['data']['attributes'])): ?>
            <div class="card">
                <div class="result-header">Scan Results</div>
                <table>
                    <tr><th>Malicious</th><td class="malicious"><?= $results['data']['attributes']['stats']['malicious'] ?? 0; ?></td></tr>
                    <tr><th>Suspicious</th><td class="suspicious"><?= $results['data']['attributes']['stats']['suspicious'] ?? 0; ?></td></tr>
                    <tr><th>Harmless</th><td class="harmless"><?= $results['data']['attributes']['stats']['harmless'] ?? 0; ?></td></tr>
                    <tr><th>Undetected</th><td class="undetected"><?= $results['data']['attributes']['stats']['undetected'] ?? 0; ?></td></tr>
                </table>
                <div class="result-header">Detailed Vendor Results</div>
                <ul>
                    <?php if (isset($results['data']['attributes']['results'])):
                        foreach ($results['data']['attributes']['results'] as $vendor => $result): ?>
                            <li><?= htmlspecialchars($vendor); ?>: <span class="<?= htmlspecialchars($result['category']); ?>"><?= htmlspecialchars($result['result']); ?></span></li>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </ul>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
