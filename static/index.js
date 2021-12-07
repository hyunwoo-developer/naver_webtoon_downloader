$(document).ready(function () {
    showAll();
});

function showAll() {
    $.ajax({
        type: 'GET',
        url: '/api/list',
        data: {},
        success: function (response) {
            let webtoons = response['webtoons']
            for (let i=0; i < webtoons.length; i++) {
                let thumbnailImgUrl = webtoons[i]['thumbnailImgUrl']
                let title = webtoons[i]['title']
                let id = webtoons[i]['id']
                let weekday = webtoons[i]['weekday']

                html = `
                        <li class="item">
                            <a class="item__thumbnail" href="/detail?id=${id}">
                                <img class="thumbnail__img" src="${thumbnailImgUrl}"/>
                                <div class="thumbnail__title">${title}</div>
                            </a>
                        </li>
                        `

                switch (weekday) {
                    case "mon":
                        $('#mon_list').append(html)
                        break
                    case "tue":
                        $('#tue_list').append(html)
                        break
                    case "wed":
                        $('#wed_list').append(html)
                        break
                    case "thu":
                        $('#thu_list').append(html)
                        break
                    case "fri":
                        $('#fri_list').append(html)
                        break
                    case "sat":
                        $('#sat_list').append(html)
                        break
                    case "sun":
                        $('#sun_list').append(html)
                        break
                }
            }
        }
    });
}