// JavaScript to handle adding the active class
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
});
