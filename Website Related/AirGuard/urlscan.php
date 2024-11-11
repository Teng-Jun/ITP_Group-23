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
                Disclaimer: Users must exercise due diligence to determine the reliability of free airdrops or Web3 project tokens. We are not responsible for any actions taken by users in the event they fall for airdrop token scams, as the decision to participate in such campaigns ultimately belongs to the users themselves.
            </p>
            <div class="URL-Description Header">
                <h1 style="text-align: center">URL Scanner</h1>
                <p class="urlscan_des">Scan a URL if you are unsure of its authenticity!</p>
            </div>
            <div class="center-container">
                <div class="form-container">
                    <form method="POST" onsubmit="showProgressMessage(event)" novalidate>
                        <div class="form-group">
                            <label for="url">Enter a URL:</label>
                            <input type="text" class="form-control" name="url" id="url" required>
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
            </div>

            <!-- Render the scan results below the form if scanData is available -->
            <?php if (!empty($scanData)): ?>
                <div class="container mt-5">
                    <h2>Scan Completed</h2>
                    <p><strong>Scanned URL:</strong> <?php echo htmlspecialchars($url); ?></p>
                    <p><strong>Status:</strong> <?php echo $scanData['status'] ?? 'N/A'; ?></p>
                    <p><strong>Malicious Detections:</strong> <?php echo $scanData['malicious'] ?? 0; ?></p>
                    <p><strong>Undetected:</strong> <?php echo $scanData['undetected'] ?? 0; ?></p>
                    <p><strong>Harmless Detections:</strong> <?php echo $scanData['harmless'] ?? 0; ?></p>

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

                    <a href="index.php" class="btn btn-primary">Back to Scan</a>
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

<script>
    document.addEventListener("DOMContentLoaded", function () {
        const form = document.querySelector("form");

        form.addEventListener("submit", function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add("was-validated");
        });
    });
</script>
