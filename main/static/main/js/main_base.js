
$(document).ready(function() {
    $(".top-menu").hover(function() {
        showSubCategoryMenu(false);
    });
    
    $(".category-menu .menu-item").hover(function() {
        showSubCategoryMenu(true);
    });
    
    $(".wrapper").hover(function() {
        showSubCategoryMenu(false);
    });
});

function showSubCategoryMenu(display) {
    var height = 0;
    var duration = 300;
    
    if (display) {
        height = 220;
        duration = 500;
    }
    
    $('.sub-category-menu').animate({ height: height }, duration, function() {
        // Animation complete.
    });
}