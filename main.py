import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://comic.naver.com/webtoon/weekday',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)



# 코딩 시작

#content > div.list_area.daily_all > div:nth-child(1) > div > h4 > span
#content > div.list_area.daily_all > div:nth-child(1) > div > ul > li:nth-child(1) > div > a > img

toontables = soup.select('#content > div.list_area.daily_all > div')
#content > div.list_area.daily_all > div:nth-child(1) > div
#content > div.list_area.daily_all > div:nth-child(2) > div
#content > div.list_area.daily_all > div:nth-child(2) > div > ul > li:nth-child(1) > div > a > img
#content > div.list_area.daily_all > div.col.col_selected > div > ul > li:nth-child(68) > a
#content > div.list_area.daily_all > div.col.col_selected > div > ul > li:nth-child(2) > a
#content > div.list_area.daily_all > div:nth-child(1) > div > h4 > span
img = soup.select('#content > div.list_area.daily_all > div > div > ul > li > div > a > img')[0]

img_lists = {}
small_title_lists = {}

week = {}

i=0
for toontable in toontables:
    imgs = toontable.select('div > ul > li > div > a > img')
    img_lists[i] = imgs
    i += 1
i=0
for toontable in toontables:
    small_titles = toontable.select('div > ul > li > div > a > img')
    small_title_lists[i] = small_titles
    i += 1

i=0
for toontable in toontables:
    week[i] = toontable.select_one('div > h4 > span').text
    i += 1


small_title_list = [[],[],[],[],[],[],[]]
for i in range(0,7):
    for a in range(0, len(small_title_lists[i])):
        small_title_list[i].append(small_title_lists[i][a]['alt'])


img_list = [[],[],[],[],[],[],[]]
for i in range(0,7):
    for a in range(0, len(img_lists[i])):
        img_list[i].append(img_lists[i][a]['src'])

i=0



# HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test_get():
   return jsonify(week,small_title_list,img_list)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)