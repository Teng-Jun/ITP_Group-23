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

include __DIR__ . '/views/header.php';
?>
    <h1>URL Scanner</h1>
    <form method="POST" onsubmit="showProgressMessage(event)">
        <label for="url">Enter a URL:</label>
        <input type="text" name="url" id="url" required>
        <label for="api">Select API:</label>
        <select name="api" id="api" required>
            <option value="virustotal">VirusTotal</option>
            <option value="checkphish">CheckPhish</option>
            <option value="ipqs">IPQualityScore (IPQS)</option>
        </select>
        <button type="submit">Scan</button>
    </form>

    <div id="progressMessage"></div>

    <?php if ($statusResult): ?>
        <div><?php include __DIR__ . '/views/results.php'; ?></div>
    <?php endif; ?>

<?php include __DIR__ . '/views/footer.php'; ?>
