$(document).ready(function () {
    showEpisodes()
});

function showEpisodes() {
    var recentPageNum = $('#recentPageNum').val()
    console.log(recentPageNum)
    for (let i = 0; i < recentPageNum; i++) {
        html = `<option value=${recentPageNum-i}>${recentPageNum-i}화</option>`
        $('#episode').append(html)
        console.log(i)
    }
}

function select_episode() {
    let id = $('#id').val()
    let episode = $('#episode').val()

    $.ajax({
        type: 'POST',
        url: '/api/select',
        data: {id_give: id, episode_give: episode},
        success: function (response) {
        }
    });
}