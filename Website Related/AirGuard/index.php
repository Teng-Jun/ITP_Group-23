<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airdrop Tracker</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="header-container">
        <?php include 'header.php'; ?>
    </div>
    <div class="wrapper">
        <main>
            <!-- Welcome Section -->
            <div class="text-center mb-5">
                <h2 class="display-4">Welcome to AirGuard!</h2>
            </div>
            <p class="learn_avoid-disclaimer">
                Disclaimer: Users must exercise due diligence to determine the reliability of free airdrops or Web3 project tokens. We are not responsible for any actions taken by users in the event they fall for airdrop token scams, as the decision to participate in such campaigns ultimately belongs to the users themselves.
            </p>
            <div class="container">
                <!-- About Section -->
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
                            <!-- Removed the reference link as per instructions -->
                            
                            <!-- Embedded Safety Tips -->
                            <div class="card mt-4 safety-tip-card">
                                <div class="card-body">
                                    <div class="alert alert-danger font-weight-bold text-center">
                                        Before collecting any Crypto Airdrop (especially free ones!) Here are a few reminders for you to take note!
                                    </div>
                                    <div class="card mb-3">
                                        <div class="card-body">
                                            <h5 class="card-title">Always Verify the Source</h5>
                                            <p class="card-text">Make sure the airdrop is from a reputable source. Check official websites or trusted platforms (Reddit, Google, Crypto.io) before participating.</p>
                                            <br>
                                            <h5 class="card-title">Be Cautious with Private Keys</h5>
                                            <p class="card-text">Never share your private keys or seed phrases. Legitimate airdrops will never ask for this information.</p>
                                            <br>
                                            <h5 class="card-title">Look for Signs of Scams</h5>
                                            <p class="card-text">Be wary of airdrops asking for an upfront payment or those promising unrealistic returns. These are likely scams.</p>
                                        </div>
                                </div>
                            </div>
                            <!-- End of Embedded Safety Tips -->
                        </div>
                    </div>
                </section>
            </div>
        </main>
        <script src="script.js"></script>
    </div>
    <!-- Footer Include -->
    <div class="footer-container">
        <?php include 'footer.php'; ?>
    </div>

    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
