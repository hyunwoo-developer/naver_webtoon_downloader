$(document).ready(function () {

});


function selectEpisode() {
    let page = $('#page').val()
    let id = $('#id').val()

    $.ajax({
        type: 'POST',
        url: '/detail',
        data: {page_num_give: page, id_give:id},
        success: function (response) {

        }
    });
}