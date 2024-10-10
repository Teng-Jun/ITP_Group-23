<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scan URL - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- Include Chart.js here -->
    <style>
        .clean { color: green; }
        .unrated { color: orange; }
        .malicious { color: red; }
    </style>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="container my-5">
        <h2>Scan a URL for Threats</h2>
        <form id="apiForm">
            <div class="form-row">
                <div class="form-group col-md-6">
                    <label for="api">Choose API:</label>
                    <select id="api" name="api" class="form-control" required>
                        <option value="virustotal">VirusTotal</option>
                        <option value="ipqs">IPQS</option>
                    </select>
                </div>
                <div class="form-group col-md-6">
                    <label for="url">Enter URL to Scan:</label>
                    <input type="text" class="form-control" name="url" id="url" placeholder="example.com" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>

        <div id="result" class="mt-4 row">
            <!-- The result section will now be divided into two columns -->
            <div id="scanResults" class="col-md-6"></div> <!-- Scan results will be displayed here -->
            <div id="chartContainer" class="col-md-6"></div> <!-- Chart will be displayed here -->
        </div>
    </div>
    <!-- Link to the external JavaScript file -->
    <script src="urlscript.js"></script>
</body>
</html>
