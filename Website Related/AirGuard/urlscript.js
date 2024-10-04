document.getElementById('apiForm').addEventListener('submit', function (e) {
e.preventDefault(); // Prevent page reload

const formData = new FormData(this);
const selectedApi = formData.get('api'); // Get the selected API (VirusTotal or IPQS)

fetch('process.php', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    // Clear previous results and chart before rendering
    document.getElementById('scanResults').innerHTML = '';
    document.getElementById('chartContainer').innerHTML = '';

    // Reset result layout classes
    document.getElementById('scanResults').className = '';
    document.getElementById('chartContainer').className = '';

    if (selectedApi === 'virustotal') {
        // VirusTotal results with two columns (scanResults + chartContainer)
        document.getElementById('scanResults').classList.add('col-md-6');
        document.getElementById('chartContainer').classList.add('col-md-6');
        document.getElementById('scanResults').innerHTML = data.result;

        // If there's chart data, render the pie chart
        if (data.chartData) {
            var ctx = document.createElement('canvas');
            ctx.id = 'resultChart';
            document.getElementById('chartContainer').appendChild(ctx);

            new Chart(ctx.getContext('2d'), {
                type: 'pie',
                data: {
                    labels: ['Clean', 'Unrated/Undetected', 'Malicious'],
                    datasets: [{
                        label: 'Analysis Results',
                        data: data.chartData,
                        backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
                                    }]
                            },
                            options: {
                                responsive: true
                            }
                        });
                    }
                } else if (selectedApi === 'ipqs') {
                    // IPQS results in a full-width layout with no chart
                    document.getElementById('scanResults').classList.add('col-12'); // Make the results take full width
                    document.getElementById('scanResults').innerHTML = data.result;

                    // Ensure the chart container is hidden for IPQS
                    document.getElementById('chartContainer').style.display = 'none';
                }
            })
            .catch(error => {
                document.getElementById('scanResults').innerHTML = 'Error: ' + error;
                document.getElementById('chartContainer').innerHTML = '';
            });
});