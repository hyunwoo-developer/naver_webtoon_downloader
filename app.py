from flask import Flask, send_file, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import os
import shutil
from urllib.request import Request, urlopen
import zipfile

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbwebtoon

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#
# data = requests.get('https://comic.naver.com/webtoon/weekday', headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')
#
# toontables = soup.select('#content > div.list_area.daily_all > div')
#
# img_lists = {}
# small_title_lists = {}
#
# week = {}
#
# idx = 0
# for toontable in toontables:
#     imgs = toontable.select('div > ul > li > div > a > img')
#     img_lists[idx] = imgs
#
#     small_titles = toontable.select('div > ul > li > div > a > img')
#     small_title_lists[idx] = small_titles
#
#     week[idx] = toontable.select_one('div > h4 > span').text
#
#     idx += 1
#
# small_title_list = [[], [], [], [], [], [], []]
# for i in range(0, 7):
#     for a in range(0, len(small_title_lists[i])):
#         small_title_list[i].append(small_title_lists[i][a]['alt'])
#
# img_list = [[], [], [], [], [], [], []]
# for i in range(0, 7):
#     for a in range(0, len(img_lists[i])):
#         img_list[i].append(img_lists[i][a]['src'])

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/main', methods=['GET'])
# def index_main():
#     return jsonify(week, small_title_list, img_list)

@app.route('/api/list', methods=['GET'])
def show_all():
    webtoons = list(db.mywebtoon.find({}, {'_id': False}))
    return jsonify({'webtoons': webtoons})

@app.route('/detail')
def detail():
    id = request.args.get("id")
    detail = db.mywebtoon.find_one({'id': id})

    cat1, cat2 = detail['category_1'], detail['category_2']
    title = detail['title']
    author = detail['author']
    thumbnailImgUrl = detail['thumbnailImgUrl']
    pageUrl = detail['pageUrl']
    desc = detail['desc']
    backgroundImgUrl = detail['backgroundImgUrl']
    recentPageNum = detail['recentPageNum']
    return render_template(
                            'detail.html',
                            id= id, cat1=cat1, cat2=cat2, title=title,
                            author=author, thumbnailImgUrl=thumbnailImgUrl,
                            pageUrl=pageUrl, desc=desc, backgroundImgUrl=backgroundImgUrl,
                            recentPageNum=recentPageNum
                            )

@app.route('/api/select', methods=['POST'])
def select_episode():
    id_receive = request.form['id_give']
    episode_receive = request.form['episode_give']

    base_url = "https://comic.naver.com/webtoon/detail?"
    url = base_url + "titleId=" + id_receive + "&no=" + episode_receive

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    images = list(soup.select('img[alt="comic content"]'))

    path = "./static/temp"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    cnt = 1
    for image in images:
        req = Request(image['src'], headers=headers)
        image_read = urlopen(req).read()

        image_open = open(path + "/" + str(cnt) + ".jpg", 'wb')
        image_open.write(image_read)
        image_open.close()
        cnt += 1

    zip_file = zipfile.ZipFile("../webtoon/webtoon.zip", "w")
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()

    return jsonify({'msg': '다운로드 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)