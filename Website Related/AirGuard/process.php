<?php
require __DIR__.'/vendor/autoload.php';

// Load environment variables
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();
$vtApiKey = $_ENV['VT_API_KEY'];  // VirusTotal API key
$ipqsApiKey = $_ENV['IPQS_API_KEY'];  // IPQS API key

$api = $_POST['api'];
$urlToScan = trim($_POST['url']);

// Normalize the URL by ensuring it has a valid protocol
if (!preg_match("~^(?:f|ht)tps?://~i", $urlToScan)) {
    $urlToScan = "https://" . $urlToScan;
}

// Validate URL
if (!filter_var($urlToScan, FILTER_VALIDATE_URL)) {
    echo json_encode(['result' => 'Invalid URL.']);
    exit;
}

$scanResult = '';
$error = '';

if ($api == 'virustotal') {
    // VirusTotal API logic
    $encodedUrl = rtrim(strtr(base64_encode($urlToScan), '+/', '-_'), '=');
    $apiUrl = "https://www.virustotal.com/api/v3/urls/{$encodedUrl}";

    $options = array(
        'http' => array(
            'header' => "x-apikey: $vtApiKey\r\n" .
                        "accept: application/json\r\n",
            'method'  => 'GET',
        ),
    );
    $context  = stream_context_create($options);
    $result = @file_get_contents($apiUrl, false, $context);

    if ($result === FALSE) {
        echo json_encode(['result' => 'Error occurred while connecting to VirusTotal.']);
    } else {
        $response = json_decode($result, true);
        if (isset($response['data'])) {
            // Initialize response categories
            $clean = $unrated = $malicious = [];
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

            // Format result
            $scanResult = "<p><strong>URL Scanned:</strong> {$urlToScan}</p>";
            $scanResult .= '<h4>Clean Engines</h4><ul>';
            foreach ($clean as $engine) {
                $scanResult .= "<li><strong>$engine:</strong> Clean</li>";
            }
            $scanResult .= '</ul>';
            $scanResult .= '<h4>Unrated/Undetected Engines</h4><ul>';
            foreach ($unrated as $engine) {
                $scanResult .= "<li><strong>$engine:</strong> Unrated/Undetected</li>";
            }
            $scanResult .= '</ul>';
            $scanResult .= '<h4>Potentially Malicious Engines</h4><ul>';
            foreach ($malicious as $engine) {
                $scanResult .= "<li><strong>$engine:</strong> Malicious</li>";
            }
            $scanResult .= '</ul>';

            // Send JSON response with chart data for VirusTotal
            echo json_encode([
                'result' => $scanResult,
                'chartData' => [count($clean), count($unrated), count($malicious)]  // Send chart data only for VirusTotal
            ]);
        } else {
            echo json_encode(['result' => 'Failed to retrieve URL analysis report from VirusTotal.']);
        }
    }
} elseif ($api == 'ipqs') {
    // IPQS API logic
    $encodedUrl = urlencode($urlToScan);
    $apiUrl = "https://www.ipqualityscore.com/api/json/url/{$ipqsApiKey}/{$encodedUrl}";

    // Send the request
    $result = @file_get_contents($apiUrl);

    if ($result === FALSE) {
        echo json_encode(['result' => 'Error occurred while connecting to IPQS API.']);
    } else {
        $response = json_decode($result, true);
        if (isset($response['success']) && $response['success']) {
            // Format result for IPQS
            $scanResult = '<h3>IPQS Domain Analysis Report</h3>';
            $scanResult .= '<p><strong>Domain:</strong> ' . htmlspecialchars($response['domain']) . '</p>';
            $scanResult .= '<p><strong>Risk Score:</strong> ' . htmlspecialchars($response['risk_score']) . '</p>';
            $scanResult .= '<p><strong>Is Parked:</strong> ' . ($response['parking'] ? 'Yes' : 'No') . '</p>';
            
            if (!empty($response['technologies'])) {
                $scanResult .= '<p><strong>Technologies:</strong> ' . implode(', ', array_map('htmlspecialchars', $response['technologies'])) . '</p>';
            } else {
                $scanResult .= '<p><strong>Technologies:</strong> None detected</p>';
            }

            // Send response (NO chartData for IPQS)
            echo json_encode(['result' => $scanResult]);
        } else {
            echo json_encode(['result' => 'Failed to retrieve IPQS analysis report.']);
        }
    }
}
