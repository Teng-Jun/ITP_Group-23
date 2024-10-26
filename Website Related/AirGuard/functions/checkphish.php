<?php
require_once __DIR__ . '/curl.php';

function handleCheckPhishScan($url) {
    global $cpApiKey;

    $response = initiateCheckPhishScan($url);

    if ($response && isset($response['jobID']) && $response['jobID'] !== 'none') {
        $jobID = $response['jobID'];
        return pollCheckPhishStatus($jobID);
    }

    return "<p>Error: Failed to initiate the scan or invalid job ID returned.</p>";
}

function initiateCheckPhishScan($url) {
    global $cpApiKey;
    $apiEndpoint = "https://developers.checkphish.ai/api/neo/scan";
    $postData = json_encode([
        "apiKey" => $cpApiKey,
        "urlInfo" => ["url" => $url],
        "scanType" => "quick"
    ]);

    $response = sendCurlRequest($apiEndpoint, ["Content-Type: application/json"], $postData);

    // Debug: Log raw response
    echo "<pre>Initiate Scan Response: " . htmlspecialchars(json_encode($response, JSON_PRETTY_PRINT)) . "</pre>";

    if (!$response || !isset($response['jobID'])) {
        die('<p>Error: Failed to initiate scan. Check API response or API key.</p>');
    }

    return $response;
}


function pollCheckPhishStatus($jobID) {
    $maxAttempts = 10;  // Adjust max attempts for polling
    $attempt = 0;
    $waitTime = 5;  // Initial wait time in seconds

    while ($attempt < $maxAttempts) {
        $statusResult = getCheckPhishStatus($jobID);

        if ($statusResult && isset($statusResult['status'])) {
            if ($statusResult['status'] === 'DONE') {
                return renderCheckPhishResults($statusResult);
            } elseif ($statusResult['status'] === 'ERROR') {
                return "<p>Error: " . htmlspecialchars($statusResult['message'] ?? 'Unknown error') . "</p>";
            } elseif ($statusResult['status'] === 'PENDING') {
                // Log each attempt for better debugging
                echo "<p>Attempt $attempt: Scan is still pending. Retrying in $waitTime seconds...</p>";
            }
        } else {
            return "<p>Failed to retrieve scan status. Please try again later.</p>";
        }

        sleep($waitTime);  // Wait before retrying
        $attempt++;
        $waitTime *= 2;  // Exponential backoff: double the wait time after each attempt
    }

    return "<p>The scan did not complete within the expected time. Please try again later.</p>";
}

function getCheckPhishStatus($jobID) {
    global $cpApiKey;
    $apiEndpoint = "https://developers.checkphish.ai/api/neo/scan/status";

    $postData = json_encode([
        "apiKey" => $cpApiKey,
        "jobID" => $jobID,
        "insights" => true
    ]);

    $response = sendCurlRequest($apiEndpoint, ["Content-Type: application/json"], $postData);

    // Debug: Log raw response and HTTP code
 #   if (!$response) {
  #      echo "<pre>No response received from CheckPhish API.</pre>";
   # } else {
    #    echo "<pre>Raw Response: " . htmlspecialchars(json_encode($response, JSON_PRETTY_PRINT)) . "</pre>";
    #}

    return $response;
}

function renderCheckPhishResults($result) {
    // Handle error field but display results if available
    if (isset($result['error']) && $result['error']) {
        echo "<p>Warning: The scan reported an issue, but here are the available results:</p>";
    }

    $html = "<h2>CheckPhish Scan Results</h2>";
    $html .= "<p><strong>Job ID:</strong> " . htmlspecialchars($result['job_id'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Status:</strong> " . htmlspecialchars($result['status'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>URL:</strong> " . htmlspecialchars($result['url'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Disposition:</strong> " . htmlspecialchars($result['disposition'] ?? 'Unknown') . "</p>";
    $html .= "<p><strong>Brand:</strong> " . htmlspecialchars($result['brand'] ?? 'N/A') . "</p>";
    $html .= "<p><strong>Resolved:</strong> " . ($result['resolved'] ? 'Yes' : 'No') . "</p>";

    if (isset($result['screenshot_path'])) {
        $html .= "<p><strong>Screenshot:</strong></p>";
        $html .= "<img src='" . htmlspecialchars($result['screenshot_path']) . "' alt='Screenshot' width='600'>";
        $html .= "<br><a href='" . htmlspecialchars($result['screenshot_path']) . "' download>Download Screenshot</a>";
    }

    $html .= "<p><strong>Insights:</strong> <a href='" . htmlspecialchars($result['insights']) . "' target='_blank'>View Insights</a></p>";

    return $html;
}
