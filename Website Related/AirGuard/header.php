<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AirGuard</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<header class="bg-primary text-white py-3">
    <div class="container-fluid d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
            <img src="image/airguard.png" alt="AirGuard Logo" class="logo mr-2" style="height: 120px; width: auto;">
        </div>
        <nav class="navbar navbar-expand-lg navbar-dark">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item"><a class="nav-link" href="index.php">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="aboutus.php">About Us</a></li>
                    <li class="nav-item"><a class="nav-link" href="current.php">Current Airdrops</a></li>
                    <li class="nav-item"><a class="nav-link" href="upcoming.php">Upcoming Airdrops</a></li>
                    <li class="nav-item"><a class="nav-link" href="tips.php">Safety Tips</a></li>
                    <li class="nav-item"><a class="nav-link" href="learn_avoid.php">Learn & Avoid Airdrop Scams</a></li>
                    <li class="nav-item"><a class="nav-link" href="urlscanio.php">Scan a URL</a></li>
                </ul>
            </div>
        </nav>
    </div>
</header>

<script>
document.addEventListener('DOMContentLoaded', function () {
    var navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(function (link) {
        // Add event listener for click
        link.addEventListener('click', function () {
            navLinks.forEach(function (navLink) {
                navLink.classList.remove('active');
            });
            link.classList.add('active');
        });

        // Set active class based on current URL
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });
});
</script>

</body>
</html>
