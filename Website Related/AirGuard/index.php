<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Tracker</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <style>
                /* Enhancements for index.php */
        .wrapper {
            width: 85%;
            max-width: 95em;
            margin: 2em auto;
            padding: 1em;
            background-color: #f5f5f5;
            box-shadow: 0 0 2em rgba(0, 0, 0, 0.1);
            flex-grow: 1;
        }

        .title-logo {
            height: 100px;
            margin-bottom: 20px;
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
                <h2 class="display-4">Welcome to AirGuard!</h2>
            </div>
            <div class="container">
                <section id="about">
                    <div class="card mb-4">
                        <div class="card-body">
                            <h3 class="card-title">What are Airdrop Tokens?</h3>
                            <p class="card-text">Airdrop tokens are a type of cryptocurrency distribution strategy used primarily by startups in the blockchain and crypto space. Companies distribute these tokens for free or as a reward for small tasks to a large number of wallet addresses, which often helps in promoting their new token, creating a community, and increasing the token's circulation.</p>
                        </div>
                    </div>
                    <div class="card mb-4">
                        <div class="card-body">
                            <h4 class="card-title">Why Participate in Airdrops?</h4>
                            <p class="card-text">Participating in airdrops can be a beneficial way for users to acquire new tokens without purchasing them. This method can lead to gaining early access to potentially valuable tokens as the project grows and develops. Additionally, it's a way to engage with new blockchain projects and understand their underlying technologies and goals.</p>
                        </div>
                    </div>
                    <div class="card mb-4">
                        <div class="card-body">
                            <h5 class="card-title">How to Safely Participate in Airdrops</h5>
                            <p class="card-text">While airdrops can offer significant rewards, they also come with risks, often associated with privacy and security. It's crucial to assess each airdrop carefully, ensuring it's from a trustworthy source. Always avoid sharing private keys or any other sensitive personal information.</p>
                            <p class="card-text">Visit our <a href="tips.php">Safety Tips</a> section to learn more about ensuring your security while participating in airdrops.</p>
                        </div>
                    </div>
                </section>
            </div>
        </main>
    </div>
</body>
</html>