<?php
function sendCurlRequest($url, $headers, $postData = null) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    if ($postData) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    // Debug: Log HTTP code and response
    echo "<p>HTTP Code: $httpCode</p>";

    if ($httpCode !== 200) {
        echo "<p>Error: Received non-200 HTTP response.</p>";
    }

    curl_close($ch);

    return json_decode($response, true);
}
