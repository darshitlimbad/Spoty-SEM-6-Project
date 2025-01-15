document.addEventListener('DOMContentLoaded', function() {
    const navMenuBtn= document.querySelector('.navbar-toggle');
    const navbarLinks= document.querySelector('.navbar-links');

    navMenuBtn.addEventListener('click', function() {
        navbarLinks.classList.toggle('active');
    });
    navbarLinks.addEventListener('click', function() {
        navbarLinks.classList.remove('active');
    });
    
});