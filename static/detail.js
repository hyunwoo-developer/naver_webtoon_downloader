$(document).ready(function () {
    showDetail();
});

function showDetail() {
    $.ajax({
        type: 'GET',
        url: '/detail',
        data: {},
        success: function (response) {
            let detail = response['detail']
            let id = detail['id']
            let title = detail['title']
            let category_1 = detail['category_1']
            let category_2 = detail['category_2']
            let author = detail['author']
            let desc = detail['desc']
            let recentPageNum = detail['recent_page_num']

            text_html = `
                        <div class="card__title" id="title">${title}</div>
                        <div class="card__author" id="author">${id}</div>
                        <div class="card__desc" id="desc">${desc}</div>
                    `

            id_html = `<input type="hidden" id="id" name="id" value="${id}"/>`

            // 화수 list
            select_html = ``
            for (let i = 1; i < recentPageNum+1; i++) {
                temp = `<option value=${i}>${i}화</option>`
                select_html += temp
            }

            $('#text').append(text_html)
            $('#selectForm').append(id_html)
            $('#episode').append(select_html)
        }
    });
}

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