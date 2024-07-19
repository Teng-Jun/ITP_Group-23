<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us - Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <style>
        /* Enhancements for aboutus.php */
        .about-section {
            padding: 60px 0;
        }

        .about-section h2 {
            color: #007BFF;
            margin-bottom: 40px;
            text-align: center;
        }

        .about-item {
            text-align: center;
            margin-bottom: 30px;
        }

        .about-item img {
            max-width: 80px;
            margin-bottom: 20px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .about-item h3 {
            font-size: 24px;
            margin-bottom: 15px;
        }

        .about-item p {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }
        
        .card {
            border: none;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
            height: 100%;
        }

        .card:hover {
            transform: translateY(-10px);
        }

        .card-body {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .card img {
            max-width: 80px;
            margin-bottom: 20px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .card-title {
            margin-top: auto;
            margin-bottom: auto;
        }

        .card-text {
            margin-top: auto;
            margin-bottom: auto;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper"> 
        <main class="about-section">
            <div class="container">
                <h1>About Us</h1>
                <div class="row">
                    <div class="col-md-4 mb-4">
                        <div class="card about-item">
                            <div class="card-body">
                                <img src="image/who.png" alt="Who We Are">
                                <h3 class="card-title">Who We Are</h3>
                                <p class="card-text">AirGuard is your top source for tracking cryptocurrency airdrops, focusing on reliability, user experience, and uniqueness.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card about-item">
                            <div class="card-body">
                                <img src="image/mission.png" alt="Our Mission">
                                <h3 class="card-title">Our Mission</h3>
                                <p class="card-text">To simplify discovering and claiming airdrops, making it accessible for everyone with detailed guides and up-to-date information.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card about-item">
                            <div class="card-body">
                                <img src="image/team.png" alt="Our Team">
                                <h3 class="card-title">Our Team</h3>
                                <p class="card-text">Founded in 2024, our passion for simplifying airdrops drives us to offer the best information. We now serve users worldwide.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="script.js"></script>
</body>
</html>
