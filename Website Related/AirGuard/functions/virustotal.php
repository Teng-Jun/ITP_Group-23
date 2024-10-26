<?php
require_once __DIR__ . '/curl.php';

function handleVirusTotalScan($url) {
    global $vtApiKey;

    $response = scanWithVirusTotal($url);
    if (isset($response['error'])) {
        return '<p>Error: ' . $response['error']['message'] . '</p>';
    }

    $analysisId = $response['data']['id'];
    $result = getVirusTotalResultsWithPolling($analysisId);
    return renderVirusTotalResults($result);
}

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

    while (true) {
        $response = sendCurlRequest($apiUrl, $headers);
        if ($response['data']['attributes']['status'] === 'completed') {
            return $response;
        }
        sleep(5);  // Wait before polling again
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