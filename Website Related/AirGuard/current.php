<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Current Airdrops - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="wrapper">
        <div class="header-container">
            <?php include 'header.php'; ?>
        </div>
        <main>
            <h2>Current Airdrops</h2>
            <div class="container">
            <section id="search">
                <form action="claim.php" method="GET" align="center">
                    <input type="text" name="search" placeholder="Search for airdrops..." aria-label="Search Airdrops">
                    <button type="submit">Search</button>
                    <button type="button" id="resetButton">Reset</button>
                </form>
            </section>
            <section id="current">
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
            </div>
        </main>
        <script src="script.js"></script>
    </div>
</body>
</html>