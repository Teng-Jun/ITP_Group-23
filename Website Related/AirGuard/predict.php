<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Prediction</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <!-- Header Section -->
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>

    <!-- Main Content Section -->
    <div class="container py-5">
        <!-- Disclaimer -->
        <p class="learn_avoid-disclaimer">
            Disclaimer: Users must exercise due diligence to ensure that the Cryptocurrency Airdrop Project is authentic and true. We are not responsible for any actions taken by users in the event they fall for airdrop token scams, as the decision to participate in such campaigns ultimately belongs to the users themselves.
        </p>
        

        <!-- Airdrop Prediction Content -->
        <div class="text-center">
            <h1 class="mb-3">Airdrop Scam Prediction</h1>
            <p class="mb-4">Enter the URL to analyze its authenticity and fetch data for prediction.</p>

            <!-- Input for the Airdrop URL -->
            <form id="urlForm" class="mb-5">
                <div class="form-group">
                    <label for="airdrop_url">Airdrop URL:</label>
                    <input type="url" id="airdrop_url" name="airdrop_url" class="form-control" placeholder="Enter the Airdrop URL" required>
                </div>
                <button type="submit" class="btn btn-primary">Fetch Airdrop Data</button>
            </form>

            <!-- Prediction Form (this gets populated automatically after fetching URL data) -->
            <form id="airdropForm" method="POST" style="display:none;" class="mb-5">
                <div class="form-group">
                    <label for="airdrop_name">Airdrop Name:</label>
                    <input type="text" id="airdrop_name" name="airdrop_name" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label for="num_of_prev_drops">Number of Previous Airdrops:</label>
                    <input type="number" id="num_of_prev_drops" name="num_of_prev_drops" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label for="presence_of_whitepaper">Presence of Whitepaper (1 if yes, 0 if no):</label>
                    <input type="number" id="presence_of_whitepaper" name="presence_of_whitepaper" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label for="requirement_count">Requirement Count:</label>
                    <input type="number" id="requirement_count" name="requirement_count" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label for="guide_length">Guide Length:</label>
                    <input type="number" id="guide_length" name="guide_length" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label for="social_media_count">Social Media Count:</label>
                    <input type="number" id="social_media_count" name="social_media_count" class="form-control" readonly>
                </div>
                <div class="form-group">
                    <label for="temperature">Temperature:</label>
                    <input type="number" id="temperature" name="temperature" class="form-control" readonly>
                </div>
                <button type="submit" class="btn btn-primary">Predict</button>
            </form>

            <div id="result" class="mb-5"></div>

            <h2 class="mb-3">Past Predictions</h2>
            <div id="pastResults"></div>
        </div>
    </div>

    <!-- Footer Section -->
    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>

    <script>
    // Load past predictions from cookies
    function loadPastPredictions() {
        const pastResults = document.cookie.split('; ').find(row => row.startsWith('pastPredictions='));
        if (pastResults) {
            const pastPredictions = JSON.parse(decodeURIComponent(pastResults.split('=')[1]));
            let resultsHtml = '';
            pastPredictions.forEach(prediction => {
                resultsHtml += `<p>${prediction.airdrop_name}: ${prediction.probability}</p>`;
            });
            document.getElementById('pastResults').innerHTML = resultsHtml;
        }
    }

    // Save predictions to cookies
    function savePrediction(airdropName, prediction) {
        const pastResults = document.cookie.split('; ').find(row => row.startsWith('pastPredictions='));
        let pastPredictions = [];
        if (pastResults) {
            pastPredictions = JSON.parse(decodeURIComponent(pastResults.split('=')[1]));
        }

        pastPredictions.push({ airdrop_name: airdropName, probability: prediction });

        // Store in cookies (for 7 days)
        document.cookie = `pastPredictions=${encodeURIComponent(JSON.stringify(pastPredictions))}; path=/; max-age=${7 * 24 * 60 * 60}`;

        // Update the past predictions section immediately after saving
        loadPastPredictions();
    }

    document.getElementById('urlForm').onsubmit = function (event) {
            event.preventDefault();

            const airdropUrl = document.getElementById('airdrop_url').value;
            const airdropUrlPattern = /^https:\/\/airdrops\.io\/[a-z0-9-]+\/?$/;

            // Blocklist of URLs that do not contain token information
            const bannedUrls = [
                "https://airdrops.io/latest/",
                "https://airdrops.io/hot/",
                "https://airdrops.io/speculative/",
                "https://airdrops.io/speculative/*",
                "https://airdrops.io/faq/",
                "https://airdrops.io/contact/",
                "https://airdrops.io/blog/",
                "https://airdrops.io/stay-safe/",
                "https://airdrops.io/nft/",
                "https://airdrops.io/holders/",
                "https://airdrops.io/forks/",
                "https://airdrops.io/exclusive/",
                "https://airdrops.io/airdrop-alert/"
            ];

            // Regex Validation
            if (!airdropUrlPattern.test(airdropUrl)) {
                alert("Invalid URL! Please enter a valid URL from airdrops.io. Example: https://airdrops.io/example-project/");
                document.getElementById('airdrop_url').focus();
                return; // Stop execution
            }

            // Check against blocklist
            if (bannedUrls.some(bannedUrl => airdropUrl.startsWith(bannedUrl))) {
                alert("The entered URL is not valid for token information. Please provide a specific token URL.");
                document.getElementById('airdrop_url').focus();
                return; // Stop execution
            }

            // Proceed with fetch operation if URL is valid and not in the blocklist
            fetch('http://13.76.25.253/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: airdropUrl })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // Show a popup alert for server-side errors
                    alert(`Error: ${data.error}`);
                    document.getElementById('result').innerText = `Error: ${data.error}`;
                } else {
                    // Populate the form fields automatically with scraped data
                    document.getElementById('airdrop_name').value = data.title;
                    document.getElementById('num_of_prev_drops').value = data.num_of_prev_drops;
                    document.getElementById('presence_of_whitepaper').value = data.presence_of_whitepaper;
                    document.getElementById('requirement_count').value = data.requirement_count;
                    document.getElementById('guide_length').value = data.guide_length;
                    document.getElementById('social_media_count').value = data.social_media_count;
                    document.getElementById('temperature').value = data.temperature;

                    // Show the prediction form
                    document.getElementById('airdropForm').style.display = 'block';
                }
            })
            .catch(error => {
                console.error("Fetch operation failed:", error);

                // Show a popup alert for fetch errors
                alert("An error occurred while fetching data. Please check the server logs.");
                document.getElementById('result').innerText = "An error occurred. Please check the server logs.";
            });
        };

    // Handle form submission to get the prediction
    document.getElementById('airdropForm').onsubmit = function (event) {
        event.preventDefault();

        const airdropName = document.getElementById('airdrop_name').value;

        // Collect form data as an object (excluding airdrop name)
        const formData = {
            num_of_prev_drops: document.getElementById('num_of_prev_drops').value,
            presence_of_whitepaper: document.getElementById('presence_of_whitepaper').value,
            requirement_count: document.getElementById('requirement_count').value,
            guide_length: document.getElementById('guide_length').value,
            social_media_count: document.getElementById('social_media_count').value,
            temperature: document.getElementById('temperature').value
        };

        // Send JSON instead of form-data for prediction
        fetch('http://13.76.25.253/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.prediction !== undefined) {
                let predictionPercentage;
                if (data.prediction === 0) {
                    predictionPercentage = "<0.01%";
                } else if (data.prediction === 1) {
                    predictionPercentage = ">99.99%";
                } else {
                    predictionPercentage = (data.prediction * 100).toFixed(2) + "%";
                }

                // Show the result only if the prediction is > 0
                document.getElementById('result').innerText = `Predicted Scam Probability: ${predictionPercentage}`;
                savePrediction(airdropName, predictionPercentage);
            } else if (data.error) {
                document.getElementById('result').innerText = "Error: " + data.error;
            }
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
            document.getElementById('result').innerText = "An error occurred. Please check the server logs.";
        });
    };

    // Load past predictions on page load
    window.onload = loadPastPredictions;
</script>

</body>
</html>
