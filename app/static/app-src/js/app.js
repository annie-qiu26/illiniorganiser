import '../scss/style.scss';
import 'bootstrap';
import 'select2';
import 'slick';


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
    })
})