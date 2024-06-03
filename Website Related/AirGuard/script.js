// JavaScript to handle adding the active class and resetting form
document.addEventListener('DOMContentLoaded', function () {
    var navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(function (link) {
        // Add event listener for click
        link.addEventListener('click', function () {
            navLinks.forEach(function (navLink) {
                navLink.parentElement.classList.remove('active');
            });
            link.parentElement.classList.add('active');
        });

        // Set active class based on current URL
        if (link.href === window.location.href) {
            link.parentElement.classList.add('active');
        }
    });

    // Handle reset button click
    var resetButton = document.getElementById('resetButton');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            window.location.href = 'upcoming.php'; // Redirects back to upcoming.php without any parameters
        });
    }
});
