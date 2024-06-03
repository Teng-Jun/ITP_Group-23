<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Airdrop Tracker</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header>
    <h1>Airdrop Tracker</h1>
    <nav>
        <ul>
            <li><a class="nav-link" href="index.php">Home</a></li>
            <li><a class="nav-link" href="#current">Current Airdrops</a></li>
            <li><a class="nav-link" href="#upcoming">Upcoming Airdrops</a></li>
            <li><a class="nav-link" href="#guide">How to Claim</a></li>
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
            <!-- Example of a current airdrop item -->
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
    <section id="upcoming">
        <h2>Upcoming Airdrops</h2>
        <div class="airdrop-container">
            <?php
            include 'dbconnection.php';
            $sql = "SELECT tle, Platform, Status FROM airdrops_data_speculative";
            $result = $conn->query($sql);
            
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo '<div class="airdrop-item">';
                    echo '<img src="placeholder.jpg" alt="Token Logo" class="airdrop-logo">';
                    echo '<div class="airdrop-info">';
                    echo '<h3>' . htmlspecialchars($row['tle']) . '</h3>';
                    echo '<p>Platform: ' . htmlspecialchars($row['Platform']) . '</p>';
                    echo '<p>Status: <span class="' . ($row['Status'] == 'Airdrop Confirmed' ? 'status-confirmed' : ($row['Status'] == 'Airdrop Unconfirmed' ? 'status-pending' : 'status-expired')) . '">' . htmlspecialchars($row['Status']) . '</span></p>';
                    echo '</div>';
                    echo '</div>';
                }
            }else{
                echo "No upcoming airdrops";
            }
            $conn->close();
            ?>
<!--             Example of an upcoming airdrop item 
            <div class="airdrop-item">
                <img src="placeholder.jpg" alt="Token Logo" class="airdrop-logo">
                <div class="airdrop-info">
                    <h3>Token Name</h3>
                    <p>Expected Drop: YYYY-MM-DD</p>
                    <p>Status: <span class="status-pending">Pending Verification</span></p>
                </div>
            </div>-->
        </div>
    </section>
</main>
<script src="script.js"></script>
</body>
</html>
