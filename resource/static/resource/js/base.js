$(document).ready(function(){
    $('.logo').hover(function(){
        $(this).attr('src', '/static/psiRbase/images/logo-hover.png');
    }, function(){
        $(this).attr('src', '/static/psiRbase/images/logo.png');
    })

    setInterval(checkScroll, 100);

    function checkScroll(){
        if ($(document).scrollTop() != 0) {
            if (!$('nav').hasClass('navbar-scrolled')){
                $('nav').addClass('navbar-scrolled');
            }
        } else {
            if ($('nav').hasClass('navbar-scrolled')){
                $('nav').removeClass('navbar-scrolled');
            }
        }
    }
});