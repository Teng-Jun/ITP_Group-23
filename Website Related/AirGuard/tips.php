<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Safety Tips - Airdrop Tracker</title>
        <link rel="stylesheet" href="styles.css">
        <link rel="icon" type="image/png" href="image/airguard-favicon-color-32.png">
        <link rel="stylesh  eet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
         <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                display: flex;
                justify-content: center;
/*                align-items: center;*/
                height: 100vh;
                background-color: white;
            }
            .container {
                text-align: center;
            }     
             
            .text-box {
                width: 60vw;
                height: 15vh;
                padding: 2em;
                border: 1em transparent;
                position: relative;
                overflow: hidden;
                transition: all 0.5s ease-in-out;
            }

            .more-text {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: white;
                transform: translateX(-100%);
                transition: transform 0.5s ease-in-out;
                padding: 1em;
                background-color: #f5f5f5;
                font-size: 1.2em;
            }

            .text-box:hover .more-text {
                transform: translateX(0);
                text-align: center;
                justify-content: center;
            }
            
            .initial-text {
                font-size: 1.5em;
                font-style: inherit;
                padding: 1em 0;
                justify-content: center;
                text-align: center;
            }
    </style>
    </head>
    <body>
        <div class="header-container">
            <?php include 'header.php'; ?>
        </div>
        <div class="wrapper">
            <main>
                <h2>Safety Tips for Airdrop Participants</h2>
                <section id="safety">
                    <div class="container">
                        <span></span>
                        <p>Before collecting any Crypto Airdrop (especially free ones!) Here are a few reminders for you to take note!</p>
                        <div class="text-box">
                            <span class="initial-text">Always Verify the Source</span>
                            <p><span class="more-text">Make sure the airdrop is from a reputable source. Check official websites or trusted platforms (Reddit, Google, Crypto.io) before participating.</span></P>
                        </div>
                        <div class="text-box">
                            <span class="initial-text">Be Cautious with Private Keys</span>
                            <p><span class="more-text">Never share your private keys or seed phrases. Legitimate airdrops will never ask for this information.</span></P>
                        </div>
                        <div class="text-box">
                            <span class="initial-text">Look for Signs of Scams</span>
                            <p><span class="more-text">Be wary of airdrops asking for an upfront payment or those promising unrealistic returns. These are likely scams.</span></P>
                        </div>
                    </div>
                </section>
            </main>
            <script src="script.js"></script>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
</html>