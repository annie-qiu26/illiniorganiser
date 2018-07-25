import '../scss/style.scss';
import 'bootstrap';
import 'select2';
import 'slick-carousel';


$(() => {
    var search = $('#search');
    search.select2({
        ajax: {
            url: '/search-suggest',
            dataType: 'json',
            delay: 250,
            },
        minimumInputLength: 1
    });
    search.on('select2:select', (e) => {
        if (e.params.data.type == 'tag') {
            window.location = '/tag/' + e.params.data.id;
        } else {
            window.location = '/rso/' + e.params.data.id;
        }
    });
    $('.responsive-slider').slick({
        accessibility: true,
        dots: true,
        arrows: true,
        infinite: false,
        speed: 300,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true,
                    arrows: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    dots: true,
                    arrows: true
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    dots: true,
                    arrows: true
                }
            }
            // You can unslick at a given breakpoint now by adding:
            // settings: "unslick"
            // instead of a settings object
        ]
    });
})