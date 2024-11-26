<?php
session_start(); // Start the session at the beginning

require __DIR__ . '/config/config.php';
require __DIR__ . '/functions/virustotal.php';
require __DIR__ . '/functions/checkphish.php';
require __DIR__ . '/functions/ipqs.php';

$statusResult = null;
$scanResults = []; // Initialize an array to hold results from all APIs

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url'])) {
    $url = filter_var($_POST['url'], FILTER_SANITIZE_URL);

    // Initialize an array to store scan results
    $scanResults = [
        'VirusTotal' => null,
        'CheckPhish' => null,
        'IPQualityScore' => null
    ];

    // Perform VirusTotal Scan
    $virustotalResult = handleVirusTotalScan($url);
    $scanResults['VirusTotal'] = $virustotalResult !== false ? $virustotalResult : ['error' => 'VirusTotal scan failed.'];

    // Perform CheckPhish Scan
    $checkphishResult = handleCheckPhishScan($url);
    $scanResults['CheckPhish'] = $checkphishResult !== false ? $checkphishResult : ['error' => 'CheckPhish scan failed.'];

    // Perform IPQualityScore (IPQS) Scan
    $ipqsResult = handleIpqsScan($url);
    $scanResults['IPQualityScore'] = $ipqsResult !== false ? $ipqsResult : ['error' => 'IPQualityScore scan failed.'];

    // Store the scanned URL and scan results in the session for display and download
    $_SESSION['scanResults'] = $scanResults;
    $_SESSION['url'] = $url;
}

// Handle Download Action
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'download') {
    if (isset($_SESSION['scanResults'])) {
        $scanResults = $_SESSION['scanResults'];
        $url = $_SESSION['url'] ?? 'Unknown URL';

        // Define a temporary directory for the zip file
        $tempDir = sys_get_temp_dir();
        $zipFile = $tempDir . '/scan_results.zip';

        // Initialize the ZipArchive class
        $zip = new ZipArchive();
        if ($zip->open($zipFile, ZipArchive::CREATE | ZipArchive::OVERWRITE) === TRUE) {
            // Add the JSON results file to the zip
            $jsonResults = json_encode(['url' => $url, 'scans' => $scanResults], JSON_PRETTY_PRINT);
            $zip->addFromString('scan_results.json', $jsonResults);

            // Add screenshot files to the zip (if available)
            foreach ($scanResults as $apiName => $result) {
                if ($apiName === 'CheckPhish' && !empty($result['screenshot_path'])) {
                    $screenshotUrl = $result['screenshot_path'];

                    // Download the screenshot
                    $screenshotContent = file_get_contents($screenshotUrl);
                    if ($screenshotContent !== false) {
                        $zip->addFromString('screenshot.png', $screenshotContent);
                    }
                }
            }

            // Close the zip file
            $zip->close();

            // Set headers to initiate the download
            header('Content-Type: application/zip');
            header('Content-Disposition: attachment; filename="scan_results.zip"');
            header('Content-Length: ' . filesize($zipFile));

            // Output the zip file
            readfile($zipFile);

            // Clean up the temporary file
            unlink($zipFile);
            exit();
        } else {
            die('Failed to create zip file.');
        }
    } else {
        // If no scan results are available
        header('Location: urlscan.php');
        exit();
    }
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upcoming Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper">
        <main>
            <p class="learn_avoid-disclaimer">
                Users must exercise due diligence and understand that the APIs provided are tools to assist in analyzing URLs but should not be trusted 100%. Always verify information independently and use multiple sources to ensure authenticity. We are not responsible for any actions taken based on the results of these scans.
            </p>
            <div class="URL-Description Header">
                <h1 class="text-center">Scan a URL</h1>
                <p class="learn_avoid-disclaimer text-center">Scan a URL if you are unsure of its authenticity!</p>
            </div>
            <div class="form-container">
                <form method="POST" onsubmit="showLoader(event);" novalidate>
                    <div class="form-group">
                        <label for="url" class="text-center">Enter a URL:</label>
                        <input type="text" class="form-control" name="url" id="url" required>
                        <div class="invalid-feedback">
                            Please enter a valid URL.
                        </div>
                    </div>

                    <div class="button-container text-center">
                        <button type="submit" class="btn btn-primary btn-lg mr-2">Scan</button>   
                        <button type="button" class="btn btn-success btn-lg" id="resetButton">Reset</button>
                    </div>    
                </form>
            </div>

            <!-- Render the scan results below the form if scanResults is available -->
            <?php if (!empty($scanResults)): ?>
            <div class="container mt-5">
                <h2 class="mb-4">Scan Results for URL: <?php echo htmlspecialchars($url); ?></h2>
                
                <?php foreach ($scanResults as $apiName => $result): ?>
                    <div class="api-results mb-5">
                        <h3><?php echo htmlspecialchars($apiName); ?> Scan Results</h3>
                        <?php if (isset($result['error'])): ?>
                            <p class="text-danger"><?php echo htmlspecialchars($result['error']); ?></p>
                        <?php else: ?>
                            <?php if ($apiName === 'VirusTotal'): ?>
                                <p><strong>Status:</strong> <?php echo htmlspecialchars($result['status']); ?></p>
                                <p><strong>Malicious Detections:</strong> <?php echo htmlspecialchars($result['malicious']); ?></p>
                                <p><strong>Undetected:</strong> <?php echo htmlspecialchars($result['undetected']); ?></p>
                                <p><strong>Harmless Detections:</strong> <?php echo htmlspecialchars($result['harmless']); ?></p>  
                            <?php elseif ($apiName === 'CheckPhish'): ?>
                                <p><strong>Status:</strong> <?php echo htmlspecialchars($result['status']); ?></p>
                                <p><strong>Job ID:</strong> <?php echo htmlspecialchars($result['job_id']); ?></p>
                                <p><strong>Disposition:</strong> <?php echo htmlspecialchars($result['disposition']); ?></p>
                                <p><strong>Brand:</strong> <?php echo htmlspecialchars($result['brand']); ?></p>
                                <p><strong>Resolved:</strong> <?php echo htmlspecialchars($result['resolved']); ?></p>

                                <?php if (!empty($result['screenshot_path'])): ?>
                                    <p><strong>Screenshot:</strong></p>
                                    <img src="<?php echo htmlspecialchars($result['screenshot_path']); ?>" alt="Screenshot" class="screenshot-image img-fluid">
                                <?php else: ?>
                                    <p>No screenshot available.</p>
                                <?php endif; ?>

                            <?php elseif ($apiName === 'IPQualityScore'): ?>
                                <p><strong>Status:</strong> <?php echo htmlspecialchars($result['status']); ?></p>
                                <p><strong>URL:</strong> <?php echo htmlspecialchars($result['url']); ?></p>
                                <p><strong>Domain:</strong> <?php echo htmlspecialchars($result['domain']); ?></p>
                                <p><strong>Risk Score:</strong> <?php echo htmlspecialchars($result['risk_score']); ?></p>
                                <p><strong>Malware Detected:</strong> <?php echo htmlspecialchars($result['malware']); ?></p>
                                <p><strong>Phishing Detected:</strong> <?php echo htmlspecialchars($result['phishing']); ?></p>
                                <p><strong>Suspicious:</strong> <?php echo htmlspecialchars($result['suspicious']); ?></p>
                                <p><strong>Spamming Detected:</strong> <?php echo htmlspecialchars($result['spamming']); ?></p>
                                <p><strong>IP Address:</strong> <?php echo htmlspecialchars($result['ip_address']); ?></p>
                            <?php endif; ?>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>

                <!-- Download and Back Buttons -->
                <div class="button-group text-center">
                    <a href="?action=download" class="btn btn-secondary btn-lg mr-2">
                        <i class="fas fa-download"></i> Download All Results
                    </a>
                </div>
            </div>
            <?php endif; ?>
        </main>
    </div>

    <!-- Footer -->
    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>

    <!-- Loader -->
    <div id="loader" class="loader-overlay" style="display: none;">
        <div class="spinner-border text-primary" role="status">
            <span class="sr-only">Processing...</span>
        </div>
        <p>Processing your request. Please wait. This might take a while...</p>
    </div>

    <!-- JavaScript Section -->
    <script src="script.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const form = document.querySelector("form");

            form.addEventListener("submit", function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                    document.getElementById("loader").style.display = "none"; // Hide loader on invalid form
                }

                form.classList.add("was-validated");
            });

            // Reset button functionality
            document.getElementById('resetButton').addEventListener('click', () => {
                window.location.href = 'urlscan.php';
            });
        });

        function showLoader(event) {
            event.preventDefault(); // Prevent form submission to show loader
            document.getElementById("loader").style.display = "flex";

            // Allow form submission after a short delay to show loader
            setTimeout(() => {
                event.target.submit();
            }, 500);
        }
    </script>
    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
