<?php
require __DIR__ . '/config/config.php';
require __DIR__ . '/functions/virustotal.php';
require __DIR__ . '/functions/checkphish.php';
require __DIR__ . '/functions/ipqs.php';

$statusResult = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url']) && isset($_POST['api'])) {
    $url = filter_var($_POST['url'], FILTER_SANITIZE_URL);
    $api = $_POST['api'];

    switch ($api) {
        case 'virustotal':
            $statusResult = handleVirusTotalScan($url);
            break;
        case 'checkphish':
            $statusResult = handleCheckPhishScan($url);
            break;
        case 'ipqs':
            $statusResult = handleIpqsScan($url);
            break;
        default:
            $statusResult = "<p>Invalid API selection.</p>";
    }
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
                                Choose an valid API!
                            </div>
                        </div>
                        <div class="button-container">
                            <button type="submit" class="btn btn-primary" style="width: 5em;">Scan</button>   
                        </div>    
                    </form>
                </div>
            </div>
        </main>
        <script src="script.js"></script>
    </div>

    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>

    <div id="progressMessage"></div>

    <?php if ($statusResult): ?>
        <div><?php include __DIR__ . '/views/results.php'; ?></div>
    <?php endif; ?>
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