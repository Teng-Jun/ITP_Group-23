<?php
require_once __DIR__ . '/../config/config.php';  // Ensure config is included
require_once __DIR__ . '/curl.php';  // Keep curl.php for sending requests

function handleIpqsScan($url) {
    global $ipqsApiKey;  // Ensure the global variable is available

    if (!$ipqsApiKey) {
        die("IPQS API Key is not set. Please check your configuration.");
    }

    $encodedUrl = urlencode($url);
    $apiEndpoint = "https://ipqualityscore.com/api/json/url/{$ipqsApiKey}/{$encodedUrl}";

    $headers = [
        "Content-Type: application/json"
    ];

    $response = sendCurlRequest($apiEndpoint, $headers);


    if (!$response || isset($response['error'])) {
        return "<p>Error: Unable to scan the URL. Please try again later.</p>";
    }

    return renderIpqsResults($response);
}

function renderIpqsResults($result) {
    $html = "<h2>IPQualityScore (IPQS) URL Scan Results</h2>";

    $html .= "<p><strong>URL:</strong> " . htmlspecialchars($result['url'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Domain:</strong> " . htmlspecialchars($result['domain'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Risk Score:</strong> " . htmlspecialchars($result['risk_score'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Malware Detected:</strong> " . ($result['malware'] ? 'Yes' : 'No') . "</p>";
    $html .= "<p><strong>Phishing Detected:</strong> " . ($result['phishing'] ? 'Yes' : 'No') . "</p>";
    $html .= "<p><strong>Suspicious:</strong> " . ($result['suspicious'] ? 'Yes' : 'No') . "</p>";
    $html .= "<p><strong>Spamming Detected:</strong> " . ($result['spamming'] ? 'Yes' : 'No') . "</p>";
    $html .= "<p><strong>IP Address:</strong> " . htmlspecialchars($result['ip_address'] ?? 'N/A') . "</p>";

    return $html;
}
