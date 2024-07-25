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

function toggleContent(uniqueId) {
    const hiddenContent = document.getElementById(uniqueId);
    if (hiddenContent) {
        const btn = hiddenContent.previousElementSibling.querySelector('.expand-btn');
        if (hiddenContent.style.display === "none" || hiddenContent.style.display === "") {
            hiddenContent.style.display = "block";
            btn.textContent = "-";
        } else {
            hiddenContent.style.display = "none";
            btn.textContent = "+";
        }
    } else {
        console.error('Element with ID ' + uniqueId + ' not found.');
    }
}
