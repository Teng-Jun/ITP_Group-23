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
        .container {
            max-width: 1200px;
            margin: auto;
            padding: 0 15px;
        }

        h2 {
            color: #007BFF;
            margin-bottom: 20px;
        }

        .card {
            border: none;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .card-body {
            padding: 20px;
        }

        .card-title {
            color: #007BFF;
            margin-bottom: 15px;
        }

        .card-text {
            font-size: 1.1em;
            line-height: 1.6;
        }

        a {
            color: #007BFF;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper"> 
        <main>
            <div class="text-center mb-5">
                <h2 class="display-4">About Us</h2>
            </div>
            <section id="about-us" class="mb-5">
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="card-title">Who We Are</h3>
                                <p class="card-text">Welcome to AirGuard, your number one source for tracking cryptocurrency airdrops. We are dedicated to giving you the very best of information, with a focus on reliability, user experience, and uniqueness.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="card-title">Our Mission</h3>
                                <p class="card-text">Our mission is to make the process of discovering and claiming airdrops easier and more accessible to everyone. We aim to provide detailed guides and up-to-date information to help you navigate the exciting world of cryptocurrency airdrops.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="card-title">Our Team</h3>
                                <p class="card-text">Founded in 2024, AirGuard has come a long way from its beginnings. When we first started out, our passion for simplifying cryptocurrency airdrops drove us to do intense research so that AirGuard can offer you the best information available. We now serve users all over the world and are thrilled that we're able to turn our passion into our own website.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="card-title">Contact Us</h3>
                                <p class="card-text">If you have any questions or comments, please don't hesitate to contact us. We are here to help and support you in your journey through the world of cryptocurrency.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="script.js"></script>
</body>
</html>
