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
            // Redirect to the current page without any query parameters
            window.location.href = window.location.pathname;
        });
    }
});
