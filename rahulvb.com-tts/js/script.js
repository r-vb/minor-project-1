/********************
header
********************/
$(".header .header__bars").on('click', function () {

    var selector = $(".header .header__nav")

    if (selector.hasClass('shown')) {
        selector.css('right', "100%");
        selector.removeClass('shown');
    } else {
        selector.css('right', "0");
        selector.addClass('shown');
    }
});

$(".header .header__nav span").on('click', function () {

    var selector = $(".header .header__nav")

    if (selector.hasClass('shown')) {
        selector.css('right', "100%");
        selector.removeClass('shown');
    } else {
        selector.css('right', "0");
        selector.addClass('shown');
    }
});

$(document).on('click', 'a[href^="#"]', function (event) {
    event.preventDefault();
    let elementId = $(event.target).attr('href');
    if (elementId == '#') return;

    $('html, body').animate({
        scrollTop: $($.attr(this, 'href')).offset().top
    }, 1000, 'swing');
});

$(window).on('scroll', () => {
    if ($(window).scrollTop() > 50) {
        $('.header-1').addClass('fixed');
    } else {
        $('.header-1').removeClass('fixed');
    }
});

$(window).on('scroll', () => {
    if ($(window).scrollTop() > 0) {
        $('.header-2').addClass('fixed');
    } else {
        $('.header-2').removeClass('fixed');
    }
});