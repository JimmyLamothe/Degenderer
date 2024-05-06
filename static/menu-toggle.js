document.addEventListener('DOMContentLoaded', function() {
    var menuToggle = document.querySelector('.menu-toggle');
    menuToggle.addEventListener('click', function() {
        var menu = document.querySelector('.menu');
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
});
