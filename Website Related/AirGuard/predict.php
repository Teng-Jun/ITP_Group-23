<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Prediction</title>
</head>
<body>
    <h1>Airdrop Scam Prediction</h1>
    <form id="airdropForm" method="POST">
        <label for="airdrop_name">Airdrop Name:</label>
        <input type="text" id="airdrop_name" name="airdrop_name" required><br><br>

        <label for="num_of_prev_drops">Number of Previous Airdrops:</label>
        <input type="number" id="num_of_prev_drops" name="num_of_prev_drops" required><br><br>

        <label for="presence_of_whitepaper">Presence of Whitepaper (1 if yes, 0 if no):</label>
        <input type="number" id="presence_of_whitepaper" name="presence_of_whitepaper" min="0" max="1" required><br><br>

        <label for="requirement_count">Requirement Count:</label>
        <input type="number" id="requirement_count" name="requirement_count" required><br><br>

        <label for="guide_length">Guide Length:</label>
        <input type="number" id="guide_length" name="guide_length" required><br><br>

        <label for="social_media_count">Social Media Count:</label>
        <input type="number" id="social_media_count" name="social_media_count" required><br><br>

        <button type="submit">Predict</button>
    </form>

    <div id="result"></div>

    <h2>Past Predictions</h2>
    <div id="pastResults"></div>

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

        document.getElementById('airdropForm').onsubmit = function (event) {
            event.preventDefault();

            const airdropName = document.getElementById('airdrop_name').value;

            // Collect form data as an object (excluding airdrop name)
            const formData = {
                num_of_prev_drops: document.getElementById('num_of_prev_drops').value,
                presence_of_whitepaper: document.getElementById('presence_of_whitepaper').value,
                requirement_count: document.getElementById('requirement_count').value,
                guide_length: document.getElementById('guide_length').value,
                social_media_count: document.getElementById('social_media_count').value
            };

            // Send JSON instead of form-data
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
