<?php
require_once 'vendor/autoload.php';

// Load .env variables
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();
$apiKey = $_ENV['VT_API_KEY']; // Ensure this matches your .env file exactly

function submitUrlToVirusTotal($url, $apiKey) {
    $data = array("url" => $url);
    $ch = curl_init('https://www.virustotal.com/api/v3/urls');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'x-apikey: ' . $apiKey
    ));
    $response = curl_exec($ch);
    curl_close($ch);
    $json = json_decode($response, true);
    // Retrieve the id of the item
    return $json['data']['id'] ?? null;
}

function retrieveVirusTotalResults($id, $apiKey) {
    $ch = curl_init('https://www.virustotal.com/api/v3/analyses/' . $id);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('x-apikey: ' . $apiKey));

    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

$results = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['url'])) {
    $urlToScan = $_POST['url'];
    $itemId = submitUrlToVirusTotal($urlToScan, $apiKey);

    if ($itemId) {
        sleep(5); // Give some time for the analysis to complete
        $results = retrieveVirusTotalResults($itemId, $apiKey);

        if (!$results || !isset($results['data']['attributes'])) {
            $error = "Failed to retrieve scan results. Please try again later.";
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
    <title>Scan URL - AirGuard</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; padding-top: 20px; }
        .form-row { margin-bottom: 20px; }
        .result-section { background: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 5px; margin-top: 20px; }
        .result-item { margin-bottom: 10px; }
        .result-header { font-size: 18px; font-weight: bold; margin-bottom: 15px; }
        .result-value { font-size: 16px; }
        .clean { color: green; }
        .malicious { color: red; }
        .suspicious { color: orange; }
        .harmless { color: green; }
        .undetected { color: gray; }
        .progress-message { color: blue; font-weight: bold; display: none; margin-top: 20px; }
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
<body onload="showErrorMessage('<?= $error ?? '' ?>')">
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
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
                    <input type="text" class="form-control" name="url" id="url" placeholder="example.com" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <div id="progressMessage" class="progress-message">Scanning in progress. Please wait...</div>
        <?php if (isset($results) && isset($results['data']['attributes'])): ?>
            <div class="result-section">
                <div class="result-header">Scan Results</div>
                <?php
                $analysisDate = $results['data']['attributes']['date'] ?? 'N/A';
                $formattedDate = $analysisDate !== 'N/A' ? date('Y-m-d H:i:s', strtotime($analysisDate)) : 'N/A';
                ?>
                <p class="result-item">Last Analysis Date: <span class="result-value"><?= htmlspecialchars($formattedDate) ?></span></p>
                <p class="result-item">Scan Time: <span class="result-value"><?= htmlspecialchars($results['data']['attributes']['scan_time'] ?? 'N/A') ?></span></p>
                <p class="result-item">Malicious: <span class="malicious"><?= $results['data']['attributes']['stats']['malicious']; ?></span></p>
                <p class="result-item">Suspicious: <span class="suspicious"><?= $results['data']['attributes']['stats']['suspicious']; ?></span></p>
                <p class="result-item">Harmless: <span class="harmless"><?= $results['data']['attributes']['stats']['harmless']; ?></span></p>
                <p class="result-item">Undetected: <span class="undetected"><?= $results['data']['attributes']['stats']['undetected']; ?></span></p>
                <div class="result-header">Detailed Vendor Results</div>
                <ul>
                    <?php if (isset($results['data']['attributes']['results'])):
                        uksort($results['data']['attributes']['results'], "strnatcasecmp");
                        foreach ($results['data']['attributes']['results'] as $vendor => $result): ?>
                            <li><?= htmlspecialchars($vendor); ?>: <span class="<?= $result['category']; ?>"><?= htmlspecialchars($result['result']); ?></span></li>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </ul>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
