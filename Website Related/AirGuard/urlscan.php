<?php
session_start(); // Start the session at the beginning

require __DIR__ . '/config/config.php';
require __DIR__ . '/functions/virustotal.php';
require __DIR__ . '/functions/checkphish.php';
require __DIR__ . '/functions/ipqs.php';

$statusResult = null;
$scanData = null; // Ensure this variable is defined

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url']) && isset($_POST['api'])) {
    $url = filter_var($_POST['url'], FILTER_SANITIZE_URL);
    $api = $_POST['api'];

    switch ($api) {
        case 'virustotal':
            $scanData = handleVirusTotalScan($url);
            break;
        case 'checkphish':
            $scanData = handleCheckPhishScan($url);
            break;
        case 'ipqs':
            $scanData = handleIpqsScan($url);
            break;
        default:
            $statusResult = "<p>Invalid API selection.</p>";
    }

    // Store the scanned URL and status result for display
    $_SESSION['scanData'] = $scanData;
    $_SESSION['url'] = $url;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Scanner</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
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
                <h1 style="text-align: center">URL Scanner</h1>
                <p class="learn_avoid-disclaimer">Scan a URL if you are unsure of its authenticity!</p>
            </div>
            <div class="form-container">
                <form method="POST" onsubmit="showProgressMessage(event); showLoader(event);" novalidate>
                    <div class="form-group">
                        <label style="text-align: center" for="url">Enter a URL:</label>
                        <input style="text-align: center" type="text" class="form-control" name="url" id="url" required>
                        <div class="invalid-feedback">
                            Enter a URL!
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="api">Select API:</label>
                        <select name="api" class="form-control" id="api" required>
                            <option value="">API</option>
                            <option value="virustotal">VirusTotal</option>
                            <option value="checkphish">CheckPhish</option>
                            <option value="ipqs">IPQualityScore (IPQS)</option>
                        </select>
                        <div class="invalid-feedback">
                            Choose a valid API!
                        </div>
                    </div>
                    <div class="button-container">
                        <button type="submit" class="btn btn-primary" style="width: 5em;">Scan</button>   
                    </div>    
                </form>
            </div>

            <!-- Render the scan results below the form if scanData is available -->
            <?php if (!empty($scanData)): ?>
            <div class="container mt-5">

                <?php if ($scanData['source'] === 'VirusTotal'): ?>
                    <h2>VirusTotal URL Scan Results</h2>
                    <p style="align-content: center"><strong>Scanned URL:</strong> <?php echo htmlspecialchars($scanData['url']); ?></p>
                    <p style="align-content: center"><strong>Status:</strong> <?php echo htmlspecialchars($scanData['status']); ?></p>
                    <p style="align-content: center"><strong>Malicious Detections:</strong> <?php echo htmlspecialchars($scanData['malicious']); ?></p>
                    <p style="align-content: center"><strong>Undetected:</strong> <?php echo htmlspecialchars($scanData['undetected']); ?></p>
                    <p style="align-content: center"><strong>Harmless Detections:</strong> <?php echo htmlspecialchars($scanData['harmless']); ?></p>  
                
                <?php elseif ($scanData['source'] === 'CheckPhish'): ?>
                    <h2>CheckPhish URL Scan Results</h2>
                    <br>
                    <p style="align-content: center"><strong>Scanned URL:</strong> <?php echo htmlspecialchars($scanData['url']); ?></p>
                    <p style="align-content: center"><strong>Status:</strong> <?php echo htmlspecialchars($scanData['status']); ?></p>
                    <p style="align-content: center"><strong>Job ID:</strong> <?php echo htmlspecialchars($scanData['job_id']); ?></p>
                    <p style="align-content: center"><strong>Disposition:</strong> <?php echo htmlspecialchars($scanData['disposition']); ?></p>
                    <p style="align-content: center"><strong>Brand:</strong> <?php echo htmlspecialchars($scanData['brand']); ?></p>
                    <p style="align-content: center"><strong>Resolved:</strong> <?php echo htmlspecialchars($scanData['resolved']); ?></p>

                    <?php if (!empty($scanData['screenshot_path'])): ?>
                        <p><strong>Screenshot:</strong></p>
                        <img src="<?php echo htmlspecialchars($scanData['screenshot_path']); ?>" alt="Screenshot" width="600" class="screenshot-image">
                        <div class="button-group">
                            <a href="<?php echo htmlspecialchars($scanData['screenshot_path']); ?>" class="btn btn-primary mt-3" download>
                                <i class="fas fa-download"></i> Download Screenshot
                            </a>
                            <a href="urlscan.php" class="btn btn-primary mt-3">
                                Back to Scan
                            </a>
                        </div>
                    <?php else: ?>
                        <p>No screenshot available.</p>
                    <?php endif; ?>


                <?php elseif ($scanData['source'] === 'IPQS'): ?>
                    <h2>IPQualityScore (IPQS) URL Scan Results</h2>
                    <br>
                    <p style="align-content: center"><strong>Status:</strong> <?php echo htmlspecialchars($scanData['status']); ?></p>
                    <p style="align-content: center"><strong>URL:</strong> <?php echo htmlspecialchars($scanData['url']); ?></p>
                    <p style="align-content: center"><strong>Domain:</strong> <?php echo htmlspecialchars($scanData['domain']); ?></p>
                    <p style="align-content: center"><strong>Risk Score:</strong> <?php echo htmlspecialchars($scanData['risk_score']); ?></p>
                    <p style="align-content: center"><strong>Malware Detected:</strong> <?php echo htmlspecialchars($scanData['malware']); ?></p>
                    <p style="align-content: center"><strong>Phishing Detected:</strong> <?php echo htmlspecialchars($scanData['phishing']); ?></p>
                    <p style="align-content: center"><strong>Suspicious:</strong> <?php echo htmlspecialchars($scanData['suspicious']); ?></p>
                    <p style="align-content: center"><strong>Spamming Detected:</strong> <?php echo htmlspecialchars($scanData['spamming']); ?></p>
                    <p style="align-content: center"><strong>IP Address:</strong> <?php echo htmlspecialchars($scanData['ip_address']); ?></p>
                <?php endif; ?>

                <!-- Display scan results table if available -->
                <?php if (!empty($scanData['results'])): ?>
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Engine</th>
                                <th>Category</th>
                                <th>Result</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($scanData['results'] as $result): ?>
                                <tr>
                                    <td><?php echo htmlspecialchars($result['engine']); ?></td>
                                    <td><?php echo htmlspecialchars($result['category']); ?></td>
                                    <td><?php echo htmlspecialchars($result['result']); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
            </div>
        <?php endif; ?>
        </main>
        <script src="script.js"></script>
    </div>

    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>
</body>
</html>

<!-- Loader -->
<div id="loader" style="display: none;">
    <div class="spinner"></div>
    <p>Processing your request. Please wait...</p>
</div>


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
    });
    
    function showLoader(event) {
        document.getElementById("loader").style.display = "flex";

        // For testing: Automatically hide loader after 3 seconds
        setTimeout(() => {
            document.getElementById("loader").style.display = "none";
        }, 3000);
    }
</script>
