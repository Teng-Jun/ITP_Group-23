<?php
require 'vendor/autoload.php';

use Dotenv\Dotenv;

// Load the .env file with error handling
try {
    $dotenv = Dotenv::createImmutable(__DIR__);
    $dotenv->load();
} catch (Exception $e) {
    die('Error loading .env file: ' . $e->getMessage());
}

// Get API keys from the environment
$vtApiKey = getenv('VT_API_KEY') ?: $_ENV['VT_API_KEY'] ?? null;
$cpApiKey = getenv('CP_API_KEY') ?: $_ENV['CP_API_KEY'] ?? null;
$usApiKey = getenv('US_API_KEY') ?: $_ENV['US_API_KEY'] ?? null;


if (!$vtApiKey || !$cpApiKey) {
    die('API keys are not set correctly in the environment.');
}

$statusResult = null; // Holds scan results
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url']) && isset($_POST['api'])) {
    $url = filter_var($_POST['url'], FILTER_SANITIZE_URL);
    $api = $_POST['api'];

    if ($api === 'virustotal') {
        $initialResponse = scanWithVirusTotal($url);
        if (isset($initialResponse['error'])) {
            $statusResult = '<p>Error: ' . $initialResponse['error']['message'] . '</p>';
        } else {
            $analysisId = $initialResponse['data']['id'];
            $statusResult = getVirusTotalResultsWithPolling($analysisId);
            $statusResult = renderVirusTotalResults($statusResult);
        }
    } elseif ($api === 'checkphish') {
        $scanResult = initiateCheckPhishScan($url);
        if ($scanResult && isset($scanResult['jobID'])) {
            $jobID = $scanResult['jobID'];
            $statusResult = pollCheckPhishStatus($jobID);
            $statusResult = renderCheckPhishResults($statusResult);
        } else {
            $statusResult = "<p>Failed to initiate the scan or jobID not found.</p>";
        }
    } elseif ($api === 'urlscan') {  // New condition for urlscan.io
        $scanResponse = initiateUrlScan($url);
        if (isset($scanResponse['uuid'])) {
            $uuid = $scanResponse['uuid'];
            $result = pollUrlScanResults($uuid);
            $statusResult = renderUrlScanResults($result);
        } else {
            $statusResult = "<p>Error initiating scan with urlscan.io.</p>";
        }
    }
}


// Functions to handle VirusTotal, CheckPhish, and cURL requests
function scanWithVirusTotal($url) {
    global $vtApiKey;
    $apiUrl = 'https://www.virustotal.com/api/v3/urls';
    $headers = ["x-apikey: $vtApiKey", 'Content-Type: application/x-www-form-urlencoded'];
    $postFields = 'url=' . urlencode($url);
    return sendCurlRequest($apiUrl, $headers, $postFields);
}

function getVirusTotalResultsWithPolling($analysisId) {
    global $vtApiKey;

    $apiUrl = "https://www.virustotal.com/api/v3/analyses/$analysisId";
    $headers = ["x-apikey: $vtApiKey"];

    // Poll the API every 5 seconds until the status is "completed"
    while (true) {
        $response = sendCurlRequest($apiUrl, $headers);

        if ($response['data']['attributes']['status'] === 'completed') {
            return $response;
        }

        // Wait for 5 seconds before polling again
        sleep(5);
    }
}

function renderVirusTotalResults($result) {
    $attributes = $result['data']['attributes'] ?? [];
    $status = $attributes['status'] ?? 'Unknown';
    $maliciousCount = $attributes['stats']['malicious'] ?? 0;
    $undetectedCount = $attributes['stats']['undetected'] ?? 0;
    $harmlessCount = $attributes['stats']['harmless'] ?? 0;

    // Ensure the scanned URL is correctly accessed from the outer 'data' key
    $scannedUrl = $result['meta']['url_info']['url'] ?? $attributes['url'] ?? 'URL not found'; 

    $permalink = $attributes['links']['self'] ?? '#';

    $html = "<h2>VirusTotal Scan Results</h2>";
    $html .= "<p><strong>Scanned URL:</strong> " . htmlspecialchars($scannedUrl) . "</p>";
    $html .= "<p><strong>Status:</strong> $status</p>";
    $html .= "<p><strong>Malicious Detections:</strong> $maliciousCount</p>";
    $html .= "<p><strong>Undetected:</strong> $undetectedCount</p>";
    $html .= "<p><strong>Harmless Detections:</strong> $harmlessCount</p>";

    if (isset($attributes['results'])) {
        $html .= '<table border="1" cellpadding="5" cellspacing="0">';
        $html .= '<tr><th>Engine</th><th>Category</th><th>Result</th></tr>';
        foreach ($attributes['results'] as $engine => $data) {
            $html .= '<tr>';
            $html .= '<td>' . htmlspecialchars($engine) . '</td>';
            $html .= '<td>' . htmlspecialchars($data['category']) . '</td>';
            $html .= '<td>' . htmlspecialchars($data['result'] ?? 'Clean') . '</td>';
            $html .= '</tr>';
        }
        $html .= '</table>';
    }

    return $html;
}



function initiateCheckPhishScan($url) {
    global $cpApiKey;
    $apiEndpoint = "https://developers.checkphish.ai/api/neo/scan";
    $postData = json_encode([
        "apiKey" => $cpApiKey,
        "urlInfo" => ["url" => $url],
        "scanType" => "full"
    ]);
    return sendCurlRequest($apiEndpoint, ["Content-Type: application/json"], $postData);
}

function pollCheckPhishStatus($jobID) {
    while (true) {
        $statusResult = getCheckPhishStatus($jobID);
        if ($statusResult) {
            if ($statusResult['status'] === 'DONE') {
                return $statusResult;
            }
            sleep(5);
        } else {
            return "<p>Failed to retrieve scan status.</p>";
        }
    }
}

function getCheckPhishStatus($jobID) {
    global $cpApiKey;
    $apiEndpoint = "https://developers.checkphish.ai/api/neo/scan/status";
    $postData = json_encode([
        "apiKey" => $cpApiKey,
        "jobID" => $jobID,
        "insights" => true
    ]);
    return sendCurlRequest($apiEndpoint, ["Content-Type: application/json"], $postData);
}

function renderCheckPhishResults($result) {
    $html = "<h2>CheckPhish Scan Results</h2>";
    $html .= "<p><strong>Job ID:</strong> " . htmlspecialchars($result['job_id']) . "</p>";
    $html .= "<p><strong>Status:</strong> " . htmlspecialchars($result['status']) . "</p>";
    $html .= "<p><strong>URL:</strong> " . htmlspecialchars($result['url']) . "</p>";
    $html .= "<p><strong>Disposition:</strong> " . htmlspecialchars($result['disposition']) . "</p>";
    $html .= "<p><strong>Brand:</strong> " . htmlspecialchars($result['brand'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Resolved:</strong> " . ($result['resolved'] ? 'Yes' : 'No') . "</p>";

    if (isset($result['screenshot_path'])) {
        $html .= "<p><strong>Screenshot:</strong></p>";
        $html .= "<img src='" . htmlspecialchars($result['screenshot_path']) . "' alt='Screenshot' width='600'>";
        $html .= "<br><a href='" . htmlspecialchars($result['screenshot_path']) . "' download>Download Screenshot</a>";
    }

    return $html;
}

function sendCurlRequest($url, $headers, $data = null) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_FAILONERROR, false);  // Prevent curl from stopping on 4xx errors

    if ($data) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode === 404) {
        // Handle 'not found' response for ongoing scans
        return null;
    }

    return json_decode($response, true);
}


function initiateUrlScan($url) {
    global $usApiKey;
    $apiEndpoint = "https://urlscan.io/api/v1/scan/";
    $postData = json_encode(["url" => $url]);

    $headers = [
        "Content-Type: application/json",
        "API-Key: $usApiKey"
    ];

    return sendCurlRequest($apiEndpoint, $headers, $postData);
}

function pollUrlScanResults($uuid) {
    $apiEndpoint = "https://urlscan.io/api/v1/result/$uuid/";
    $headers = ["Content-Type: application/json"];

    // Poll every 5 seconds up to a maximum timeout (e.g., 60 seconds)
    $maxAttempts = 12;  // 12 attempts = 1 minute (5s each)
    $attempt = 0;

    while ($attempt < $maxAttempts) {
        $result = sendCurlRequest($apiEndpoint, $headers);

        // If valid result is returned, process it
        if ($result && isset($result['task'])) {
            return $result;  // Success, return the result
        }

        // If result isn't ready, wait and try again
        sleep(5);
        $attempt++;
    }

    // If the scan did not complete within the timeout period
    return [
        'error' => 'The scan did not complete in a timely manner. Please try again later.'
    ];
}


function renderUrlScanResults($result) {
    if (isset($result['error'])) {
        return "<p>Error: " . htmlspecialchars($result['error']) . "</p>";
    }

    $html = "<h2>urlscan.io Scan Results</h2>";

    // Format the scan date properly
    $rawDate = $result['task']['time'] ?? 'N/A';
    $formattedDate = $rawDate !== 'N/A' ? formatDateTime($rawDate) : 'N/A';

    $html .= "<p><strong>Scan UUID:</strong> " . htmlspecialchars($result['task']['uuid'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Scan Date:</strong> " . htmlspecialchars($formattedDate) . "</p>";
    $html .= "<p><strong>URL:</strong> " . htmlspecialchars($result['page']['url'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Domain:</strong> " . htmlspecialchars($result['page']['domain'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>IP Address:</strong> " . htmlspecialchars($result['page']['ip'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Country:</strong> " . htmlspecialchars($result['page']['country'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>ASN:</strong> " . htmlspecialchars($result['page']['asn'] ?? 'N/A') . "</p>";

    $html .= "<p><strong>Status Code:</strong> " . htmlspecialchars($result['stats']['status'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Malicious:</strong> " .
             (isset($result['verdicts']['overall']['malicious']) && $result['verdicts']['overall']['malicious'] ? 'Yes' : 'LIKELY not malicious') .
             "</p>";

    return $html;
}

function formatDateTime($isoDate) {
    $dateTime = new DateTime($isoDate);
    $dateTime->setTimezone(new DateTimeZone('Asia/Singapore'));  // Set to local time zone
    return $dateTime->format('d M Y, h:i A');  // Example: "26 Oct 2024, 06:15 PM"
}



?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Scanner</title>
    <script>
        function showProgressMessage(event) {
            event.preventDefault(); // Prevent immediate form submission

            const messageDiv = document.getElementById('progressMessage');
            messageDiv.innerHTML = "<p>Scanning in progress. Please wait...</p>";

            document.querySelector('button[type="submit"]').disabled = true; // Disable button

            // Delay the form submission to show the message
            setTimeout(() => {
                event.target.submit();
            }, 100); // Adjust the delay if needed
        }
    </script>
</head>
<body>
    <h1>URL Scanner</h1>
    <form method="POST" onsubmit="showProgressMessage(event)">
        <label for="url">Enter a URL:</label>
        <input type="text" name="url" id="url" required>
        <label for="api">Select API:</label>
        <select name="api" id="api" required>
            <option value="virustotal">VirusTotal</option>
            <option value="checkphish">CheckPhish</option>
            <option value="urlscan">Urlscan.io</option>
        </select>
        <button type="submit">Scan</button>
    </form>

    <!-- Progress Message -->
    <div id="progressMessage"></div>

    <?php if ($statusResult): ?>
        <div>
            <?= $statusResult ?>
        </div>
    <?php endif; ?>
</body>
</html>

