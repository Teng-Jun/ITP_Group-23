

<?php
session_start();

// Retrieve the current URL
$currentUrl = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

// Set the default header
$headerText = "Scan Completed";

// Change the header based on the URL
if (strpos($currentUrl, 'urlcompleted.php') !== false) {
    $headerText = "URL Scan Results";
}

if (!isset($_SESSION['scanData'])) {
    // Redirect back to the main page if there's no scan data
    header("Location: index.php");
    exit;
}

$scanData = $_SESSION['scanData'];
$url = $_SESSION['url'];

// Clear session data after displaying to prevent reloading issues
unset($_SESSION['scanData']);
unset($_SESSION['url']);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $headerText; ?></title>
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
            <div class="container">
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
        </main>
    </div>
</body>
</html>
