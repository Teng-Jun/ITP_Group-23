<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Current Airdrops - Airdrop Tracker</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header>
    <h1>Airdrop Tracker</h1>
    <nav>
        <ul>
            <li><a class="nav-link" href="index.php">Home</a></li>
            <li><a class="nav-link" href="current.php">Current Airdrops</a></li>
            <li><a class="nav-link" href="upcoming.php">Upcoming Airdrops</a></li>
            <li><a class="nav-link" href="tips.php">Safety Tips</a></li>
        </ul>
    </nav>
</header>
<main>
    <section id="search">
        <input type="text" placeholder="Search for airdrops..." aria-label="Search Airdrops">
        <button type="submit">Search</button>
    </section>
    <section id="current">
        <h2>Current Airdrops</h2>
        <div class="airdrop-container">
            <!-- Database connection and data fetching logic will go here -->
            <!-- Static content example shown, replace with PHP database results -->
            <div class="airdrop-item">
                <img src="placeholder.jpg" alt="Token Logo" class="airdrop-logo">
                <div class="airdrop-info">
                    <h3>Token Name</h3>
                    <p>Drop Date: YYYY-MM-DD</p>
                    <p>Status: <span class="status-safe">Safe</span></p>
                </div>
            </div>
        </div>
    </section>
</main>
<script src="script.js"></script>
</body>
</html>
