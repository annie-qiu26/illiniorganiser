import '../scss/style.scss';
import 'bootstrap';

$(() => {

    $('.menu-icon').click(() => {
      $(this).toggleClass('active')
      $('.sidebar').toggleClass('active')
    })

})